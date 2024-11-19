from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.service import AuthService, UserCreateModel, UserLoginModel, Token
from src.config.database import get_session

auth_router = APIRouter()
auth_service = AuthService()

@auth_router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    try:
        return await auth_service.signup(user_data, session)
    except HTTPException as e:
        raise e  

@auth_router.post("/login", response_model=Token)
async def login(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    try:
        return await auth_service.login(login_data, session)
    except HTTPException as e:
        raise e 

