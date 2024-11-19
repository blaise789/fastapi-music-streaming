from pydantic import BaseModel

class UserCreateModel(BaseModel):
    username: str
    email: str
    password: str

class UserLoginModel(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
