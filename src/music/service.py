from sqlalchemy.ext.asyncio import AsyncSession
from src.music.models import Song
from src.music.schemas import SongCreateModel, SongUpdateModel
from fastapi import HTTPException, status
from sqlalchemy.future import select

class SongService:

    async def create_song(self, song_data: SongCreateModel, session: AsyncSession):
        song = Song(**song_data)
        session.add(song)
        await session.commit()
        await session.refresh(song)
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
