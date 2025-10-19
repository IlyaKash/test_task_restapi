from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.device import Device
from schemas.device import DeviceCreate, DevicePatch, DeviceUpdate, DeviceList

class DeviceCRUD:
    def __init__(self, session: AsyncSession):
        self.session=session
    
    async def creaet(self, device: DeviceCreate) -> Device:
        db_device =  Device(**device.model_dump())
        self.session.add(db_device)
        await self.session.commit()
        await self.session.refresh(db_device)
        return db_device
    
    async def get(self, device_id: int) -> Device | None:
        result = await self.session.execute(select(Device).where(Device.id==device_id))
        return result.scalar_one_or_none()
    
    async def get_all(self) -> DeviceList:
        result=await self.session.execute(select(Device))
        return result.scalars().all()
    
    async def update(self, device_id: int, device_update: DeviceUpdate) -> Device | None:
        device=await self.get(device_id)
        if device:
            update_data=device_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(device, field, value)
            await self.session.commit()
            await self.session.refresh(device)
        return device

    async def patch(self, device_id: int, device_patch: DevicePatch) -> Device | None:
        device=await self.get(device_id)
        if device:
            update_data=device_patch.model_dump(exclude_none=True, exclude_unset=True)
            if not update_data:
                raise ValueError("No fields to update")
            for field, value in update_data.items():
                setattr(device, field, value)
            
            await self.session.commit()
            await self.session.refresh(device)
        return device
    
    async def delete(self, device_id: int) -> bool:
        device = await self.session.get(device_id)
        if device:
            await self.session.delete(device)
            await self.session.commit()
            return True
        return False
    
    async def get_by_name(self, name:str) -> Device | None:
        result= await self.session.execute(select(Device).where(Device.name==name))
        return result.scalar_one_or_none()
    
    async def remove_battery_from_device(self, device_id: int, battery_id: int) -> bool:
        """Удалить батарею из устройства"""
        from app.crud.battery import BatteryCRUD
        
        battery_crud = BatteryCRUD(self.session)
        battery = await battery_crud.get(battery_id)
        
        if battery and battery.device_id == device_id:
            return await battery_crud.delete(battery_id)
        
        return False