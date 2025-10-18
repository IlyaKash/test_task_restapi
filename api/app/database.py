from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings

DATABASE_URL=f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

class Base(DeclarativeBase):
    pass

engine=create_async_engine(
    DATABASE_URL,
    echo=True,
)
async_session_maker=async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session()->AsyncGenerator[AsyncSession, None]:
    """
    Генератор асинхронных сессий
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()