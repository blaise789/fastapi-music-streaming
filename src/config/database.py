from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.models import UserModel
from src.config.settings import *
from typing import AsyncGenerator

from sqlalchemy.orm import sessionmaker
engine=create_async_engine(Config.DATABASE_URL,echo=True)
async def initdb():
   print(Config.DATABASE_URL)
   async with engine.begin() as conn:
          await conn.run_sync(UserModel.metadata.create_all)
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session