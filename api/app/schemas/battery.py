from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, ClassVar
import re

class BatteryBase(BaseModel):
    """Базовая схема для аккумуляторной батареи"""
    
    # Название АКБ в пределах от 1 до 100 символов
    name: str = Field(
        ...,
        min_length=1, 
        max_length=100,
        examples=["Battery_001", "AKB_Main"],
        description="Unique battery name"
    )
    
    # Номинальное напряжение
    nominal_voltage: float = Field(
        ..., 
        gt=0,
        le=1000,  # Максимальное значение
        examples=[12.0, 24.0, 48.0, 220.0, 400.0],
        description="Nominal voltage in volts"
    )
    
    # Остаточная емкость
    residual_capacity: float = Field(
        ...,
        ge=0, 
        le=100,
        examples=[95.0, 50.5, 23.7, 100.0],
        description="Residual capacity in percentage"
    )
    
    # Срок службы
    service_life: int = Field(
        ...,
        gt=0,
        le=3650,  # допустим 10 лет максимум
        examples=[365, 730, 1825],
        description="Service life in days"
    )

    @field_validator('name')
    def validate_name_format(cls, v: str) -> str:
        """Проверяет формат имени батареи"""
        if not re.match(r'^[a-zA-Z0-9_\- ]+$', v):
            raise ValueError('Name can only contain letters, numbers, spaces, hyphens and underscores')
        if v.strip() != v:
            raise ValueError('Name cannot have leading or trailing spaces')
        return v

    @field_validator('service_life')
    def validate_service_life_reasonable(cls, v: int) -> int:
        if v > 3650:
            raise ValueError('Service life should not exceed 10 years (3650 days)')
        return v


class BatteryCreate(BatteryBase):
    """Схема для создания новой батареи"""
    #ID устройства к которому подключен АКБ
    device_id: int = Field(
        ... ,
        examples=[1, 2, 3],
        description="The identifier of the device to which the battery is linked"
    )


class BatteryUpdate(BaseModel):
    """Схема для полного обновления батареи"""
    name: str = Field(
        ...,
        min_length=1, 
        max_length=100,
        examples=["Updated_Battery_001"],
        description="Unique battery name"
    )
    nominal_voltage: float = Field(
        ..., 
        gt=0,
        le=1000,
        examples=[24.0],
        description="Nominal voltage in volts"
    )
    residual_capacity: float = Field(
        ...,
        ge=0, 
        le=100,
        examples=[80.0],
        description="Residual capacity in percentage"
    )
    service_life: int = Field(
        ...,
        gt=0,
        le=3650,
        examples=[500],
        description="Service life in days"
    )
    device_id: int = Field(
        ...,
        examples=[1, 2, 3],
        description="The identifier of the device to which the battery is linked"
    )


class BatteryPatch(BaseModel):
    """Схема для частичного обновления батареи"""
    name: Optional[str] = Field(
        None,
        min_length=1, 
        max_length=100,
        examples=["Renamed_Battery"],
        description="Unique battery name"
    )
    nominal_voltage: Optional[float] = Field(
        None, 
        gt=0,
        le=1000,
        examples=[48.0],
        description="Nominal voltage in volts"
    )
    residual_capacity: Optional[float] = Field(
        None,
        ge=0, 
        le=100,
        examples=[75.5],
        description="Residual capacity in percentage"
    )
    service_life: Optional[int] = Field(
        None,
        gt=0,
        le=3650,
        examples=[600],
        description="Service life in days"
    )
    device_id: Optional[int] = Field(
        None,
        examples=[5],
        description="The identifier of the device to which the battery is linked"
    )



class Battery(BatteryBase):
    """Схема для ответа API с батареей"""
    id: int = Field(
        ...,
        examples=[1, 2, 3],
        description="Unique battery ID"
    )
    device_id: int = Field(
        ...,
        examples=[1, 2, 3],
        description="The identifier of the device to which the battery is linked"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Battery_001",
                "nominal_voltage": 12.0,
                "residual_capacity": 95.5,
                "service_life": 365,
                "device_id": 1,
            }
        }
    )

#Для ответа списка батарей
class BatteryList(BaseModel):
    devices: List[Battery]
    total: int
    skip: int = 0
    limit: int = 100

class BatteryResponse(BaseModel):
    success: Optional[bool]=True
    data: Optional[Battery]
    message: Optional[str]=""