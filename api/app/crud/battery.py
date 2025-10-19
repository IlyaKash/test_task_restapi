from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.battery import Battery
from models.device import Device
from schemas.battery import BatteryCreate, BatteryUpdate, BatteryPatch

class BatteryCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, battery: BatteryCreate) -> Battery:
        # Проверяем, что устройство существует
        device = await self.session.get(Device, battery.device_id)
        if not device:
            raise ValueError(f"Device with id {battery.device_id} not found")
        
        # Проверяем, что у устройства меньше 5 батарей
        batteries_count = await self.count_by_device(battery.device_id)
        if batteries_count >= 5:
            raise ValueError("Device cannot have more than 5 batteries")
        
        db_battery = Battery(**battery.model_dump())
        self.session.add(db_battery)
        await self.session.commit()
        await self.session.refresh(db_battery)
        return db_battery
    
    async def get(self, battery_id: int) -> Battery | None:
        result = await self.session.execute(select(Battery).where(Battery.id == battery_id))
        return result.scalar_one_or_none()
    
    async def get_all(self) -> list[Battery]:
        result = await self.session.execute(select(Battery))
        return result.scalars().all()
    
    async def get_by_device(self, device_id: int) -> list[Battery]:
        """Получить все батареи устройства"""
        result = await self.session.execute(
            select(Battery).where(Battery.device_id == device_id)
        )
        return result.scalars().all()
    
    async def update(self, battery_id: int, battery_update: BatteryUpdate) -> Battery | None:
        battery = await self.get(battery_id)
        if battery:
            # Если меняется device_id, проверяем новое устройство
            if battery_update.device_id != battery.device_id:
                device = await self.session.get(Device, battery_update.device_id)
                if not device:
                    raise ValueError(f"Device with id {battery_update.device_id} not found")
                
                # Проверяем, что у нового устройства меньше 5 батарей
                batteries_count = await self.count_by_device(battery_update.device_id)
                if batteries_count >= 5:
                    raise ValueError("New device cannot have more than 5 batteries")
            
            update_data = battery_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(battery, field, value)
            
            await self.session.commit()
            await self.session.refresh(battery)
        return battery
    
    async def patch(self, battery_id: int, battery_patch: BatteryPatch) -> Battery | None:
        """Частичное обновление батареи"""
        battery = await self.get(battery_id)
        if battery:
            update_data = battery_patch.model_dump(exclude_unset=True, exclude_none=True)
            
            if not update_data:
                raise ValueError("No fields to update")
            
            # Если меняется device_id, проверяем новое устройство
            if 'device_id' in update_data and update_data['device_id'] != battery.device_id:
                new_device_id = update_data['device_id']
                device = await self.session.get(Device, new_device_id)
                if not device:
                    raise ValueError(f"Device with id {new_device_id} not found")
                
                # Проверяем, что у нового устройства меньше 5 батарей
                batteries_count = await self.count_by_device(new_device_id)
                if batteries_count >= 5:
                    raise ValueError("New device cannot have more than 5 batteries")
            
            for field, value in update_data.items():
                setattr(battery, field, value)
            
            await self.session.commit()
            await self.session.refresh(battery)
        return battery
    
    async def delete(self, battery_id: int) -> bool:
        battery = await self.get(battery_id)
        if battery:
            await self.session.delete(battery)
            await self.session.commit()
            return True
        return False
    
    async def count_by_device(self, device_id: int) -> int:
        """Посчитать количество батарей у устройства"""
        result = await self.session.execute(
            select(func.count(Battery.id)).where(Battery.device_id == device_id)
        )
        return result.scalar() or 0
    
    async def get_low_capacity_batteries(self, threshold: float = 20.0) -> list[Battery]:
        """Получить батареи с низкой емкостью"""
        result = await self.session.execute(
            select(Battery).where(Battery.residual_capacity < threshold)
        )
        return result.scalars().all()
    
    async def get_need_replacement_batteries(self) -> list[Battery]:
        """Получить батареи, требующие замены (емкость < 10% или срок службы < 30 дней)"""
        result = await self.session.execute(
            select(Battery).where(
                (Battery.residual_capacity < 10) | (Battery.service_life < 30)
            )
        )
        return result.scalars().all()
    
    async def reassign_battery(self, battery_id: int, new_device_id: int) -> Battery | None:
        """Переподключить батарею к другому устройству"""
        battery = await self.get(battery_id)
        if not battery:
            return None
        
        # Проверяем новое устройство
        device = await self.session.get(Device, new_device_id)
        if not device:
            raise ValueError(f"Device with id {new_device_id} not found")
        
        # Проверяем лимит батарей у нового устройства
        batteries_count = await self.count_by_device(new_device_id)
        if batteries_count >= 5:
            raise ValueError("New device cannot have more than 5 batteries")
        
        # Обновляем device_id
        battery.device_id = new_device_id
        await self.session.commit()
        await self.session.refresh(battery)
        return battery
    
    async def get_battery_stats(self) -> dict:
        """Получить статистику по батареям"""
        # Общее количество
        total_result = await self.session.execute(select(func.count(Battery.id)))
        total = total_result.scalar()
        
        # Средняя емкость
        avg_capacity_result = await self.session.execute(select(func.avg(Battery.residual_capacity)))
        avg_capacity = round(avg_capacity_result.scalar() or 0, 2)
        
        # Количество с низкой емкостью
        low_capacity_result = await self.session.execute(
            select(func.count(Battery.id)).where(Battery.residual_capacity < 20)
        )
        low_capacity = low_capacity_result.scalar()
        
        # Количество требующих замены
        need_replacement_result = await self.session.execute(
            select(func.count(Battery.id)).where(
                (Battery.residual_capacity < 10) | (Battery.service_life < 30)
            )
        )
        need_replacement = need_replacement_result.scalar()
        
        return {
            "total_batteries": total,
            "average_capacity": avg_capacity,
            "low_capacity_count": low_capacity,
            "need_replacement_count": need_replacement
        }