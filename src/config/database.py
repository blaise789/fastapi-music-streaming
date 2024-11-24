from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from src.auth.models import UserModel
from sqlalchemy.ext.declarative import declarative_base
from src.config.settings import *
from typing import AsyncGenerator

from sqlalchemy.orm import sessionmaker
engine=create_async_engine(Config.DATABASE_URL,echo=True)
async def initdb():
   print(Config.DATABASE_URL)
   async with engine.begin() as conn:
          await conn.run_sync(SQLModel.metadata.create_all)
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
Base=declarative_base()        