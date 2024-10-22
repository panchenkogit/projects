# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import SQL_DB

# Создаем асинхронный движок
engine = create_async_engine(SQL_DB, connect_args={"check_same_thread": False})

# Создаем асинхронную сессию
AsyncSessionLocal = sessionmaker(autoflush=False, bind=engine, class_=AsyncSession)

# Определяем базовый класс для моделей
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
