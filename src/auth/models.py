from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__="users"
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    is_active: bool = Field(default=True)
