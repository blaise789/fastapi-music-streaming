from typing import List, Optional
from sqlalchemy import Column, ForeignKey, func
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg

class Song(SQLModel, table=True):
    __tablename__ = "songs"
    
    id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, nullable=False, autoincrement=True))
    title: Optional[str] = None
    artist: Optional[str] = None
    duration: Optional[int] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None
    file_url: str
    is_active: bool = Field(sa_column=Column(pg.BOOLEAN, default=True))

    cover_url: str = Field(sa_column=Column(pg.VARCHAR, default="/static/song_covers/default.png"))
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP, default=func.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now(), onupdate=func.now()))
    
    album_id: Optional[int] = Field(default=None, sa_column=Column(pg.INTEGER, ForeignKey("albums.id")))
    playlist_id: Optional[int] = Field(default=None,sa_column=Column(pg.INTEGER, ForeignKey("playlists.id")))
    album: Optional["Album"] = Relationship(back_populates="songs")  # Fixed annotation
    playlist: Optional["Playlist"] = Relationship(back_populates="songs") # Fixed annotation
    def __repr__(self) -> str:
        return f"<Song(title={self.title}, artist={self.artist})>"

class Album(SQLModel, table=True):
    __tablename__ = "albums"

    id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, nullable=False, autoincrement=True))
    title: str
    release_date: datetime
    songs: List["Song"] = Relationship(back_populates="album")  # Fixed annotation
    

    # user=Relationship("User",back_populates="playlists")
class Playlist(SQLModel,table=True):
    __tablename__ = "playlists"
    id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, nullable=False, autoincrement=True))
    title: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now(), onupdate=func.now()))
    songs: List["Song"] = Relationship(back_populates="playlist")  
