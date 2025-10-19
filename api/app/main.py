from fastapi import FastAPI
from routers.battery import router as battery_router
from routers.device import router as device_router

app = FastAPI(
    title="Battery Monitoring API",
    description="API для мониторинга аккумуляторных батарей и устройств",
    version="1.0.0"
)

app.include_router(device_router, prefix="/api/devices", tags=["devices"])
app.include_router(battery_router, prefix="/api/batteries", tags=["batteries"])

@app.get("/")
async def root():
    return {
        "message": "Battery Monitoring API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}