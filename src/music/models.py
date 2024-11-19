from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Song(SQLModel, table=True):
    __tablename__ = "songs"

    id: Optional[int] = Field(default=None, primary_key=True)

    title: str = Field(..., max_length=255)

    artist: Optional[str] = Field(default=None, max_length=255)

    duration: Optional[int] = Field(default=None)

    release_date: Optional[datetime] = Field(default=None)

    genre: Optional[str] = Field(default=None, max_length=100)

    is_active: bool = Field(default=True)

   
