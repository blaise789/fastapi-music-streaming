from sqlalchemy import func
from sqlmodel import SQLModel, Field,Column
import sqlalchemy.dialects.postgresql as pg

from datetime import datetime
class Song(SQLModel, table=True):
    __tablename__ = "songs"
    
    id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, nullable=False, autoincrement=True))
    
    title: str  
    artist: str   
    duration: int  
    release_year: int 
    genre: str  
    is_active: bool = Field(sa_column=Column(pg.BOOLEAN, default=True))
    
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now(), onupdate=func.now()))
    
    def __repr__(self) -> str:
        return f"<SongModel(title={self.title}, artist={self.artist})>"

