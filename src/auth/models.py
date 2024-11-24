from datetime import datetime
from sqlmodel import Relationship, SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import func

class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    
    id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, nullable=False, autoincrement=True))
    
    username: str
    email: str
    hashed_password: str
    
    is_active: bool = Field(sa_column=Column(pg.BOOLEAN, default=True))
    
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now(), onupdate=func.now()))

    # artists=Relationship("Song",back_populates="albums")
    # playlists=Relationship("Playlist",back_populates="user")
    
    def __repr__(self) -> str:
        return f"<UserModel(username={self.username})>"

    