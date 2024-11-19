from typing import Optional
from sqlalchemy import func
from sqlmodel import SQLModel, Field,Column
import sqlalchemy.dialects.postgresql as pg

from datetime import datetime
class Song(SQLModel, table=True):
    __tablename__ = "songs"
    
    id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, nullable=False, autoincrement=True))
    
    title:  Optional[str]  
    artist: Optional[str]   
    duration: Optional[int]  
    release_year: Optional[int] 
    genre: Optional[str]  
    is_active: Optional[bool] = Field(sa_column=Column(pg.BOOLEAN, default=True))
    
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now(), onupdate=func.now()))
    
    def __repr__(self) -> str:
        return f"<SongModel(title={self.title}, artist={self.artist})>"

