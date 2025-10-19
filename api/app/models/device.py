from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, validates
from database import Base

class Device(Base):
    """
    Модель данных сущности Устройство\n
    Содержит:\n
    id - идентификатор(первичный ключ)\n
    name - уникальное название\n
    firmware_version - версия прошивки\n
    is_active - состояние вкл/выкл

    Device Entity Data Model\n
    Contains:\n
    id - identifier (primary key)\n
    name - unique name\n
    firmware_version - firmware version\n
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