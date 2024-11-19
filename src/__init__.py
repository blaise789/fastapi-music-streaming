from contextlib import asynccontextmanager
from fastapi import FastAPI

from .auth.routes import *
from .music.routes import *

version = "v1"
prefix=f"api/{version}"



app = FastAPI(
    title="Bookly",
    version=version,
)


app.include_router(auth_router,prefix=f"/{prefix}/auth")
app.include_router(music_router,prefix=f"/{prefix}/songs")
