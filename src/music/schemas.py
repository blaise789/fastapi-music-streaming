
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Model to create a new song (use this in POST request)
class SongCreateModel(BaseModel):
    title: str
    artist: Optional[str] = None
    duration: Optional[int] = None
    release_date: Optional[datetime] = None
    genre: Optional[str] = None

    class Config:
        orm_mode = True  # Tells Pydantic to treat this as an ORM model

# Model to update an existing song (use this in PUT/PATCH request)
class SongUpdateModel(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    duration: Optional[int] = None
    release_date: Optional[datetime] = None
    genre: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True  # Tells Pydantic to treat this as an ORM model

# Model to return a song's details (use this in GET requests)
class SongResponseModel(SongCreateModel):
    id: int
    is_active: bool

    class Config:
        orm_mode = True  # Tells Pydantic to treat this as an ORM model
