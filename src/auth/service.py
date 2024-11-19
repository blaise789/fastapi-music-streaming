import bcrypt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import UserModel
from src.config.database import get_session
import jwt
from src.config.settings import Config
from src.auth.pydantic_schemas import *

# JWT Configuration
SECRET_KEY = Config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    def __init__(self):
        pass

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def create_access_token(self, data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def signup(self, user_data: UserCreateModel, session: AsyncSession) -> Token:
        stmt = select(UserModel).where(UserModel.username == user_data.username)
        result = await session.execute(stmt)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken.")
        
        hashed_password = self.hash_password(user_data.password)
        new_user = UserModel(username=user_data.username, email=user_data.email, hashed_password=hashed_password)
        session.add(new_user)
        try:
          await session.commit()
        except Exception as e:
          print(e)
          await session.rollback()
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user.")

        token_data = {"sub": user_data.username}
        access_token = self.create_access_token(data=token_data)
        return Token(access_token=access_token, token_type="bearer")

    async def login(self, login_data: UserLoginModel, session: AsyncSession) -> Token:
        stmt = select(UserModel).where(UserModel.username == login_data.username)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user is None or not self.verify_password(login_data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        token_data = {"sub": login_data.username}
        access_token = self.create_access_token(data=token_data)
        return Token(access_token=access_token, token_type="bearer")
