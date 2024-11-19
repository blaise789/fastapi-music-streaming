# import uuid
# import bcrypt
# from fastapi import Depends, HTTPException, Header
# from database import get_db
# from middleware.auth_middleware import auth_middleware
from .models import *
from .pydantic_schemas import *
from fastapi import APIRouter
# from sqlalchemy.orm import Session
# import jwt
# from sqlalchemy.orm import joinedload

auth_router = APIRouter()


@auth_router.get("/")
async def hello():
    return "hello world"