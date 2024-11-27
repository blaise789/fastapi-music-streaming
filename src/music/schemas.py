
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Model to create a new song (use this in POST request)
class SongCreateModel(BaseModel):
    title: str
    artist: Optional[str] = None
    duration: Optional[int] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None

   

class SongUpdateModel(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    duration: Optional[int] = None
    release_date: Optional[int] = None
    genre: Optional[str] = None
    is_active: Optional[bool] = None

   

class SongResponseModel(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    duration: Optional[int] = None
    release_date: Optional[int] = None
    genre: Optional[str] = None
    is_active: Optional[bool] = None
    # id: int
    # is_active: bool

class PlaylistCreateModel(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True  # This allows Pydantic to work with SQLAlchemy ORM models


class PlaylistUpdateModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class PlaylistResponseModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    songs: List[str] = []  # This could be a list of SongResponseModel or a list of song titles

    class Config:
        orm_mode = True
