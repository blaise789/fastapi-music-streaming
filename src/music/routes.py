from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.music.models import Playlist
from src.music.service import SongService
from src.music.schemas import SongCreateModel, SongUpdateModel, SongResponseModel
from src.config.database import get_session
from .schemas import PlaylistCreateModel,PlaylistUpdateModel

music_router = APIRouter()
song_service = SongService()

@music_router.post("/", response_model=SongResponseModel, status_code=status.HTTP_201_CREATED)
async def create_song(song_data: SongCreateModel, session: AsyncSession = Depends(get_session)):
    return await song_service.create_song(song_data, session)
    
@music_router.get("/", response_model=list[SongResponseModel])
async def get_all_songs(session: AsyncSession = Depends(get_session)):
    return await song_service.get_all_songs(session)

@music_router.get("/{song_id}", response_model=SongResponseModel)
async def get_song(song_id: int, session: AsyncSession = Depends(get_session)):
    return await song_service.get_song(song_id, session)

@music_router.patch("/{song_id}", response_model=SongResponseModel)
async def update_song(song_id: int, song_data: SongUpdateModel, session: AsyncSession = Depends(get_session)):
    return await song_service.update_song(song_id, song_data, session)

@music_router.delete("/{song_id}", response_model=dict)
async def delete_song(song_id: int, session: AsyncSession = Depends(get_session)):
    return await song_service.delete_song(song_id, session)

@music_router.post("/playlists/", response_model=Playlist)
async def create_playlist(playlist: PlaylistCreateModel, session: AsyncSession = Depends(get_session)):
    return await song_service.create_playlist(playlist, session)

@music_router.get("/playlists/", response_model=list[Playlist])
async def list_playlists(session: AsyncSession = Depends(get_session)):
    return await song_service.list_playlists(session)

@music_router.get("/playlists/{playlist_id}", response_model=Playlist)
async def get_playlist(playlist_id: int, session:AsyncSession = Depends(get_session)):
    return await song_service.get_playlist(playlist_id, session)

@music_router.put("/playlists/{playlist_id}", response_model=Playlist)
async def update_playlist(playlist_id: int, updated_playlist: PlaylistUpdateModel, session: AsyncSession = Depends(get_session)):
    return await song_service.update_playlist(playlist_id, updated_playlist, session)

@music_router.delete("/playlists/{playlist_id}")
async def delete_playlist(playlist_id: int, session: AsyncSession = Depends(get_session)):
    return await song_service.delete_playlist(playlist_id, session)
