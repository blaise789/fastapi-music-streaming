from datetime import datetime
from sqlalchemy import Integer
from sqlmodel import SQLModel, Field,Column
import sqlalchemy.dialects.postgresql as pg


class UserModel(SQLModel, table=True):
    __tablename__="users"
    id: int = Field(sa_column=Column(Integer,primary_key=True,nullable=False,autoincrement=True))
    username: str
    email: str
    hashed_password: str
    is_active: bool = Column(default=True)
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now()))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now()))
    def __repr__(self)->str:
        return f"<Book {self.title}>"