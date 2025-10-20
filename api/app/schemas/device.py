from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, ClassVar
from .battery import Battery

class DeviceBase(BaseModel):
    #Нзвание устройства в пределах от 1 до 100 символов, содержит примеры и описание
    name: str = Field(
        ...,
        min_length=1, 
        max_length=100,
        examples=["Device_001", "Sensor_Ilya"],
        description="Unique device name"
    )
    #Версия прошивки в пределах от 1 до 50 символов, содержит примеры и описание
    firmware_version: str = Field(
        ...,
        min_length=1, 
        max_length=50,
        examples=["1.0.0", "2.1.3-beta"],
        description="Device firmware version"
    )
    #вкл/выкл устройство, по умолчанию True
    is_active: bool = Field(
        default=True,
        description="Device operational status"
    )

    #Валидация полей
    @field_validator('name')
    def validate_name(cls, v):
        """Проверяем, что имя содержит только допустимые символы"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Name can only contain alphanumeric characters, underscores and hyphens')
        return v.strip()

    @field_validator('firmware_version')
    def validate_version_format(cls, v):
        """Базовая проверка формата версии"""
        if not all(c.isalnum() or c in '.-_' for c in v):
            raise ValueError('Version can only contain alphanumeric characters, dots, hyphens and underscores')
        return v

    class Config:
        orm_mode = True

class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    """Для полного обновления устройства"""
    name: str = Field(
        ...,
        min_length=1, 
        max_length=100,
        examples=["Updated_Device"],
        description="Unique device name"
    )
    firmware_version: str = Field(
        ...,
        min_length=1, 
        max_length=50,
        examples=["2.0.0"],
        description="Device firmware version"
    )
    is_active: bool = Field(
        ...,
        description="Device operational status"
    )


class DevicePatch(BaseModel):
    """Для частичного обновления устройства"""
    name: Optional[str] = Field(
        None,
        min_length=1, 
        max_length=100,
        examples=["Renamed_Device"],
        description="Unique device name"
    )
    firmware_version: Optional[str] = Field(
        None,
        min_length=1, 
        max_length=50,
        examples=["1.5.0"],
        description="Device firmware version"
    )
    is_active: Optional[bool] = Field(
        None,
        description="Device operational status"
    )


class Device(DeviceBase):
    """Схема для ответа API"""
    id: int = Field(..., examples=[1, 2, 3], description="Unique device ID")
    #Содержит список АКБ
    batteries: List['Battery'] = Field(
        default_factory=list,
        description="List of associated batteries"
    )

    #Допольниельная валидация поля batteries
    @field_validator('batteries')
    def validate_max_batteries(cls, v):
        if len(v)>5:
            raise ValueError('Device cannot have more than 5 battaries')
        return v


    class Config:
        from_attributes = True
        json_schema_extra: ClassVar[dict] = {
            "example": {
                "id": 1,
                "name": "Main_Sensor",
                "firmware_version": "1.2.3",
                "is_active": True,
                "batteries": [],
            }
        }

#Для ответа списка устройств
class DeviceList(BaseModel):
    devices: List[Device]
    total: int
    skip: int = 0
    limit: int = 100


class DeviceResponse(BaseModel):
    success: Optional[bool]=True
    data: Optional[Device]
    message: Optional[str]=""