from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine,create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.models import *
from src.config import Config
from sqlalchemy.orm import sessionmaker
engine=create_async_engine(Config.DATABASE_URL,echo=True)
async def initdb():
   async with engine.begin() as conn:
          await conn.run_sync(User.metadata.create_all)
from typing import AsyncGenerator
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session