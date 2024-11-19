
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Model to create a new song (use this in POST request)
class SongCreateModel(BaseModel):
    title: str
    artist: Optional[str] = None
    duration: Optional[int] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None

    class Config:
        orm_mode = True  

class SongUpdateModel(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    duration: Optional[int] = None
    release_date: Optional[int] = None
    genre: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True 

class SongResponseModel(SongCreateModel):
    id: int
    is_active: bool

    class Config:
        orm_mode = True 
