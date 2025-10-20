from fastapi import APIRouter, Depends, HTTPException, Query, status

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.schemas.battery import Battery, BatteryCreate, BatteryList, BatteryUpdate, BatteryPatch, BatteryResponse
from app.crud.battery import BatteryCRUD


router= APIRouter()

router.post(
    "/",
    response_model=BatteryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую батарею",
    description="Создать новую батарею и привязать к устройству"
)
async def create_battery(
        battery: BatteryCreate,
        db: AsyncSession=Depends(get_async_session)
):
    crud=BatteryCRUD(db)

    try:
        new_battery=await crud.create(battery)
        return BatteryResponse(
            success=True,
            data=new_battery,
            message="Battery created successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
@router.get(
    "/",
    response_model=BatteryList,
    summary="Получить все батареи",
    description="Возвращает список всех батарей"
)
async def read_batteries(
    skip: int=Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int=Query(100, ge=1, le=1000, description="Лимит записей"),
    db: AsyncSession=Depends(get_async_session)
):
    crud=BatteryCRUD(db)

    batteries=await crud.get_all()
    return BatteryList(
        devices=batteries[skip:skip+limit],
        total=len(batteries),
        skip=skip,
        limit=limit
    )

@router.get(
    "/{battery_id}",
    response_model=BatteryResponse,
    summary="Получить батарею по ID",
    description="Возвращает батарею по ее идентификатору"
)
async def read_battery(
    battery_id: int,
    db: AsyncSession= Depends(get_async_session)
):
    crud=BatteryCRUD(db)
    battery=await crud.get(battery_id)

    if not battery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Battery not found"
        )
    
    return BatteryResponse(
        success=True,
        data=battery
    )

@router.put(
    "/{battery_id}",
    response_model=BatteryResponse,
    summary="Полльносью обновляет батарею",
    description="Полнсотью обновляет все поля батаери"
)
async def update_battery(
    battery_id: int,
    battery_update: BatteryUpdate,
    db: AsyncSession=Depends(get_async_session)
):
    crud=BatteryCRUD(db)

    try:
        battery=await crud.update(battery_id, battery_update)
        if not battery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Battery not found"
            )
        return BatteryResponse(
            success=True,
            data=battery,
            message="Battery updated successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch(
    "/{battery_id}",
    response_model=BatteryResponse,
    summary="Частично обновляет батарею",
    description="Обновляте только указанные поля батареи"
)
async def patch_battery(
    battery_id: int,
    battery_patch: BatteryPatch,
    db: AsyncSession=Depends(get_async_session)
):
    crud=BatteryCRUD(db)
    try:
        battery=await crud.patch(battery_id, battery_patch)
        if not battery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Battery not found"
            )
        return BatteryResponse(
            success=True,
            data=battery,
            message="Battery patched successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete(
    "/{battery_id}",
    status_code=status.HTTP_200_OK,
    summary="Удаляет батарею",
    description="Удаляет батарею"
)
async def delete_battery(
    battery_id: int,
    db: AsyncSession=Depends(get_async_session)
):
    crud=BatteryCRUD(db)
    success=await crud.delete(battery_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Battery not found"
        )
    return {
        "success" : True,
        "message" : "Battery deleted successfully"
    }

@router.post(
    "/{battery_id}/ressign/{device_id}",
    response_model=BatteryResponse,
    summary="Переподключить батарею",
    description="Переподключает батарею к другому устройству"
)
async def ressign_battery(
    battery_id:int,
    device_id: int,
    db: AsyncSession=Depends(get_async_session)
):
    crud = BatteryCRUD(db)

    try:
        battery=await crud.reassign_battery(battery_id, device_id)
        if not battery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Battery not found"
            )
        return BatteryResponse(
            success=True,
            data=battery,
            message="Battery ressigned successfylly"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
@router.get(
    "/stats/summary",
    response_model=dict,
    summary="Статистка по батареям",
    description="Возвращает общую статистку по батареям"
)
async def get_battery_stats(
    db: AsyncSession=Depends(get_async_session)
):
    crud=BatteryCRUD(db)
    stats=await crud.get_battery_stats()
    return stats

@router.get(
    "/alerts/low_capacity",
    response_model=List[Battery],
    summary="Батареи с низкой емкостью",
    description="Возвращает батарею с остаточной емкастью ниже указанного порога"
)
async def get_low_capacity_batteries(
    threshold: float = Query(20.0, ge=0, le=100, description="Порог емкости в процентах"),
    db: AsyncSession=Depends(get_async_session)
):
    crud=BatteryCRUD(db)
    batteries=await crud.get_low_capacity_batteries(threshold)
    return batteries

@router.get(
    "/alerts/need_replacment",
    response_model=List[Battery],
    summary="Батареи требующие замены",
    description="Возвращает батареи которые требуют замены"
)
async def get_need_replacement_batteries(
    db: AsyncSession=Depends(get_async_session)
):
    crud=BatteryCRUD(db)
    batteries=await crud.get_need_replacement_batteries()
    return batteries