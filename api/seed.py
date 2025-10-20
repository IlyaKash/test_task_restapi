import asyncio
from app.database import async_session_maker
from app.crud.device import DeviceCRUD
from app.crud.battery import BatteryCRUD
from app.schemas.device import DeviceCreate
from app.schemas.battery import BatteryCreate


async def seed_data():
    async with async_session_maker() as session:
        device_crud = DeviceCRUD(session)
        battery_crud = BatteryCRUD(session)

        print("Заполняем базу данных тестовыми данными...")

        # Создаём устройства
        devices_data = [
            DeviceCreate(name="POS-terminal-1", firmware_version="v1.0.2", is_active=True),
            DeviceCreate(name="POS-terminal-2", firmware_version="v1.0.5", is_active=True),
            DeviceCreate(name="Barcode-scanner", firmware_version="v2.0.1", is_active=False),
        ]

        devices = []
        for d in devices_data:
            existing = await device_crud.get_by_name(d.name)
            if not existing:
                device = await device_crud.create(d)
                devices.append(device)
                print(f"Устройство '{device.name}' создано.")
            else:
                print(f"Устройство '{d.name}' уже существует, пропускаем.")
                devices.append(existing)

        # Создаём батареи
        batteries_data = [
            BatteryCreate(name="Battery_AA", nominal_voltage=1.5, residual_capacity=80.0, service_life=200, device_id=devices[0].id),
            BatteryCreate(name="Battery_AAA", nominal_voltage=1.2, residual_capacity=50.0, service_life=120, device_id=devices[0].id),
            BatteryCreate(name="Battery_18650", nominal_voltage=3.7, residual_capacity=15.0, service_life=45, device_id=devices[1].id),
            BatteryCreate(name="LiPo_1000mAh", nominal_voltage=3.7, residual_capacity=5.0, service_life=10, device_id=devices[2].id),
        ]

        for b in batteries_data:
            existing_batteries = await battery_crud.get_all()
            if not any(x.name == b.name for x in existing_batteries):
                await battery_crud.create(b)
                print(f"Батарея '{b.name}' добавлена.")
            else:
                print(f"Батарея '{b.name}' уже существует, пропускаем.")

        print("\nБаза данных успешно заполнена тестовыми данными!")


if __name__ == "__main__":
    asyncio.run(seed_data())
