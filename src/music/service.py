from sqlalchemy.ext.asyncio import AsyncSession
from src.music.models import Playlist, Song
from src.music.schemas import *
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

class SongService:

    async def create_song(self, song_data: SongCreateModel, session: AsyncSession):
        song_data=song_data.model_dump()
        song = Song(**song_data)
        session.add(song)
        await session.commit()
        await session.refresh(song)
        print(song)
        return song

    async def get_all_songs(self, session: AsyncSession):
        result = await session.execute(select(Song).filter(Song.is_active == True))
        songs = result.scalars().all()
        return songs

    async def get_song(self, song_id: int, session: AsyncSession):
        result = await session.execute(select(Song).filter(Song.id == song_id, Song.is_active == True))
        song = result.scalar_one_or_none()
        if song is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
        return song

    async def update_song(self, song_id: int, song_data: SongUpdateModel, session: AsyncSession):
        song = await self.get_song(song_id, session)
        for key, value in song_data.dict(exclude_unset=True).items():
            setattr(song, key, value)
        await session.commit()
        await session.refresh(song)
        return song

    async def delete_song(self, song_id: int, session: AsyncSession):
        song = await self.get_song(song_id, session)
        song.is_active = False  # Soft delete
        await session.commit()
        return {"message": "Song successfully deleted"}

    
    async def create_playlist(self,playlist: PlaylistCreateModel, session: AsyncSession):
        playlist_data = playlist.model_dump()
        playlist=Playlist(**playlist_data)
        session.add(playlist)
        await session.commit()
        await session.refresh(playlist)
        return playlist
    async def add_song_to_playlist(self, song_id, playlist_id,session:AsyncSession):
        playlist:Playlist = await self.get_playlist(playlist_id, session)
        song = await self.get_song(song_id, session)
        print(playlist.songs)
        playlist.songs.append(song)
        await session.commit()
        return {"message": "Song added to playlist successfully"}
    async def list_playlists(self,session: AsyncSession):
        result = await session.execute(select(Playlist))
        playlists = result.scalars().all()
        return playlists
    async def get_playlist(self,playlist_id: int, session: AsyncSession):
        result= await session.execute(select(Playlist).options(joinedload(Playlist.songs)).filter(Playlist.id==playlist_id) )
        playlist =result.scalars().first()
        print(playlist.songs)
        if  playlist is None:
            raise HTTPException(status_code=404, detail="Playlist not found")
        return playlist
    
    async def update_playlist(self,playlist_id: int, updated_playlist: Playlist, session: AsyncSession):
        playlist = session.get(Playlist, playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        for key, value in updated_playlist.dict(exclude_unset=True).items():
            setattr(playlist, key, value)
        session.commit()
        session.refresh(playlist)
        return playlist
    
    async def delete_playlist(self,playlist_id: int, session: AsyncSession):
        playlist = session.get(Playlist, playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        session.delete(playlist)
        session.commit()
        return {"message": "Playlist deleted successfully"}