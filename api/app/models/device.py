from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, validates
from app.database import Base

class Device(Base):
    """
    Модель данных сущности Устройство
    Содержит:
    id - идентификатор(первичный ключ)
    name - уникальное название
    firmware_version - версия прошивки
    is_active - состояние вкл/выкл

    Device Entity Data Model
    Contains:
    id - identifier (primary key)
    name - unique name
    firmware_version - firmware version
    is_active - on/off status
    """
    __tablename__="devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    firmware_version = Column(String, nullable=False)
    is_active =  Column(Boolean, default=True)

    #Связь с аккумуляторами (ограничение по тз в 5)
    #Relationship with batteries (requirements for 5)
    battaries= relationship("Battery", back_populates="device", cascade="all, delete-orphan")

    @validates('batteries')
    def validate_batteries_count(self, key, battery):
        if len(self.battaries) > 5:
            raise ValueError("Device cannot have more than 5 batteries")