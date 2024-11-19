from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.config.database import initdb

from .auth.routes import *
from .music.routes import *

version = "v1"
prefix=f"api/{version}"

@asynccontextmanager
async def lifespan(fastApi:FastAPI):
    print("application started")
    await initdb()
    yield
    print("application stopped")
    
app = FastAPI(
    title="Bookly",
    version=version,
    lifespan=lifespan
)


app.include_router(auth_router,prefix=f"/{prefix}/auth")
app.include_router(music_router,prefix=f"/{prefix}/songs")
