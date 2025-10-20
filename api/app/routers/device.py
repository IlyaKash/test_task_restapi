from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.schemas.device import Device, DeviceCreate, DevicePatch, DeviceUpdate, DeviceList, DeviceResponse
from app.schemas.battery import Battery, BatteryCreate
from app.crud.device import DeviceCRUD
from app.crud.battery import BatteryCRUD

router= APIRouter()

@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="СОздать новое устройство",
    description="Создать новое устройство с уникальным именем"
)
async def create_device(
    device: DeviceCreate,
    db:AsyncSession=Depends(get_async_session)
):
    crud=DeviceCRUD(db)
    
    #Проверка на уникальность имени
    existing_device= await crud.get_by_name(device.name)
    if existing_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device with this name already exists"
        )
    
    try:
        new_device=await crud.create(device)
        return DeviceResponse(
            success=True,
            data=new_device,
            message="Device created successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=DeviceList,
    summary="Получить все устройства",
    description="Возвращает список всех устройств"
)
async def read_devices(
    skip: int = Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
    db: AsyncSession=Depends(get_async_session)
):
    crud=DeviceCRUD(db)
    devices=await crud.get_all()
    return DeviceList(
        devices=devices[skip:skip+limit],
        total=len(devices),
        skip=skip,
        limit=limit
    )

@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Получить устройство по ID",
    description="Возвращает устройство по идентификатору"
)
async def read_device(
    device_id:int,
    db: AsyncSession=Depends(get_async_session)
):
    crud=DeviceCRUD(db)
    device=await crud.get(device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    return DeviceResponse(
        success=True,
        data=device
    )


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Польностью обновоить устройство",
    description="Полностью обновляет все поля устройства"
)
async def update_device(
    device_id: int,
    device_update: DeviceUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    crud=DeviceCRUD(db)

    #Проверка на уникальность имени
    existing_device= await crud.get_by_name(device_update.name)
    if existing_device and existing_device.id != device_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device with this name already exists"
        )
    
    try:
        #Если устройства с такими id не существует вернет None
        device= await crud.update(device_id, device_update)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
        
        return DeviceResponse(
            success=True,
            data=device,
            message="Device updated successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Частично обновить устройство",
    description="Обновляет только указанные поля устройства"
)
async def patch_device(
    device_id: int,
    device_patch: DevicePatch,
    db: AsyncSession=Depends(get_async_session)
):
    crud=DeviceCRUD(db)

    #При patch имя может быть не указано поэтому проверяем на уникальность имени только если оно существует
    if device_patch.name:
        existing_device= await crud.get_by_name(device_patch.name)
        if existing_device and existing_device.id != device_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Device with this name already exists"
            )
        
    try:
        device=await crud.patch(device_id, device_patch)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
        return DeviceResponse(
            success=True,
            data=device,
            message="Device patched successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete(
    "/{device_id}",
    status_code=status.HTTP_200_OK,
    summary="Удаляет устройство",
    description="Удаляет устройство и все связанные с ним батареи"
)
async def delete_device(
    device_id: int,
    db: AsyncSession=Depends(get_async_session)
):
    crud = DeviceCRUD(db)

    success=await crud.delete(device_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    return {
        "success" : True, "message": "Device deleted successfully"
    }

@router.post(
    "/{device_id}/batteries",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить батарею к устройству",
    description="Добавляет новую батарею к указанному устройству"
)
async def add_battery_to_device(
    device_id: int,
    battery: BatteryCreate,
    db: AsyncSession = Depends(get_async_session)
):
    device_crud=DeviceCRUD(db)
    battery_crud=BatteryCRUD(db)

    #Поверяем существование устройства
    device=await device_crud.get(device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    try:
        battery.device_id=device_id
        new_battery=await battery_crud.create(battery)
        
        update_device=await device_crud.get(device_id)
        return DeviceResponse(
            success=True,
            data=update_device,
            message="Battery added to device success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
@router.get(
    "/{device_id}/batteries",
    response_model=List[Battery],
    summary="Получить батареи утсройства",
    description="Возвращает все батареи, подключенные к устройству"
)
async def get_device_batteries(
    device_id:int,
    db:AsyncSession=Depends(get_async_session)
):
    battery_crud=BatteryCRUD(db)
    batteries=await battery_crud.get_by_device(device_id)
    return batteries

@router.delete(
    "/{device_id}/batteries/{battery_id}",
    summary="Удалить батарею из устройства",
    description="Удаляет батаерю из устройства"
)
async def remove_battery_from_device(
    device_id:int,
    battery_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    device_crud=DeviceCRUD(db)
    success=await device_crud.remove_battery_from_device(device_id, battery_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Battery not found or not associated with this device"
        )
    return {
        "success" : True,
        "message" : "Battery removed from device successfully"
    }

    