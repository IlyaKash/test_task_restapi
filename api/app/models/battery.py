from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Battery(Base):
    """
    Модель данных сущности АКБ
    Содержит:
    id - идентификатор(первичный ключ)
    name - уникальное название
    nominal_voltage - номинальное напряжение
    residual_capacity - остаточная емкость
    service_life - срок службы в днях
    device_id - внешний ключ на таблицу devices

    Battery Entity Data Model
    Contains:
    id - identifier (primary key)
    name - unique name
    nominal_voltage - nominal voltage
    residual_capacity - residual capacity
    service_life - service life in days
    device_id - foreign key to the devices table
    """
    __tablename__="batteries"

    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, unique=True, index=True, nullable=False)
    nominal_voltage = Column(Float,nullable=False)
    residual_capacity=Column(Float, nullable=False)
    service_life=Column(Integer, nullable=False)

    device_id=Column(Integer, ForeignKey('devices.id', ondelete="CASCADE"))
    device=relationship("Device", back_populates="batteries")