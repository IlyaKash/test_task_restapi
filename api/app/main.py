from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.routers.battery import router as battery_router
from app.routers.device import router as device_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app = FastAPI(
    title="Battery Monitoring API",
    description="API для мониторинга аккумуляторных батарей и устройств",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
