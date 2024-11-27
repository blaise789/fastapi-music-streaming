import pandas as pd
import requests
from datetime import datetime
from random import choice, randint
from sqlalchemy import create_engine
from src.music.models import Song, Playlist 
from sqlmodel import SQLModel, Session

genres = ["Pop", "Rock", "Hip-Hop", "Classical", "Jazz", "Electronic", "Country", "R&B", None]
artists = ["Artist A", "Artist B", "Artist C", "Artist D", None]
file_urls = [f"/static/songs/song_{i}.mp3" for i in range(1, 101)] + [None]
cover_urls = [f"/static/song_covers/cover_{i}.png" for i in range(1, 101)] + [None]
playlist_names = [f"Playlist {i}" for i in range(1, 101)] 

DATABASE_URL = "postgresql://postgres:Blaise%40123@127.0.0.1:5432/music_db"
engine = create_engine(DATABASE_URL)
from sqlmodel import select

def retrieve_data_from_db():
    with Session(engine) as session:
        songs_query = session.exec(select(Song)).all()
        
        playlists_query = session.exec(select(Playlist)).all()

    songs_data = []
    for song in songs_query:
        song_data = {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "duration": song.duration,
            "release_year": song.release_year,
            "genre": song.genre,
            "file_url": song.file_url,
            "cover_url": song.cover_url,
            "is_active": song.is_active,
            "created_at": song.created_at,
            "updated_at": song.updated_at,
            "playlist_id": song.playlist_id 
        }
        songs_data.append(song_data)

    playlists_data = []
    for playlist in playlists_query:
        playlist_data = {
            "id": playlist.id,
            "name": playlist.name,
            "description": playlist.description,
            "created_at": playlist.created_at,
            "updated_at": playlist.updated_at
        }
        playlists_data.append(playlist_data)

    songs_df = pd.DataFrame(songs_data)
    playlists_df = pd.DataFrame(playlists_data)
    songs_df,playlists_df=preprocess_data(songs_df, playlists_df)

    return songs_df, playlists_df

def get_data_for_csv_concat():
    song_api = 'http://localhost:8000/api/v1/songs/'  
    response = requests.get(song_api)
    songs_data = response.json()
    print(songs_data)
    basic_info = ['id', 'title', 'artist', 'genre', 'file_url', 'cover_url']
    technical_info = ['duration', 'release_year', 'is_active', 'created_at', 'updated_at']

    basic_info_data = []
    technical_info_data = []

    for song in songs_data:
        basic_data = {key: song[key] for key in basic_info if key in song}
        technical_data = {key: song[key] for key in technical_info if key in song}

        basic_info_data.append(basic_data)
        technical_info_data.append(technical_data)

    basic_info_df = pd.DataFrame(basic_info_data)
    technical_info_df = pd.DataFrame(technical_info_data)

    basic_info_df.to_csv('basic_info_songs.csv', index=False)
    technical_info_df.to_csv('technical_info_songs.csv', index=False)

    concatenated_df = pd.concat([basic_info_df, technical_info_df], axis=1)

    concatenated_df.to_csv('concatenated_songs.csv', index=False)

    print(f"Concatenated DataFrame shape: {concatenated_df.shape}")

    return concatenated_df


    

def preprocess_data(songs_df, playlists_df):
    song_freq=songs_df["genre"].value_counts(normalize=True)
    songs_df["genre_freq"]=songs_df["genre"].map(song_freq)
    songs_df.drop('genre', axis=1)
   
    
    songs_df.fillna({'title':songs_df['title'].mode()[0]}, inplace=True)
    songs_df.fillna({'artist':songs_df["artist"].mode()[0]}, inplace=True)
    songs_df.fillna({'duration':songs_df['duration'].mode()[0]}, inplace=True)
    songs_df.fillna({'release_year':songs_df['release_year'].mode()[0]}, inplace=True)
    songs_df.fillna({"genre_freq":songs_df["genre_freq"].mode()[0]}, inplace=True)
    songs_df.fillna({'file_url':f'/static/songs/{songs_df["title"]}.mp3'}, inplace=True)
    songs_df.fillna({'sover_url':'/static/songs/covers/song_cover_avatar.png'}, inplace=True)

    current_year = datetime.now().year
    songs_df['song_age'] = current_year - songs_df['release_year']
  

    playlists_df.fillna({'description':'No description available'}, inplace=True)

    # songs_df['release_year'] = songs_df['release_year'].astype(int)
    # songs_df['duration'] = songs_df['duration'].astype(float)

    return songs_df, playlists_df

def create_data_and_save_to_db():
    song_records = []
    playlist_records = []

    with Session(engine) as session:
        for _ in range(500000):
            title = choice([f"Song {randint(1, 1000000)}", None])
            artist = choice(artists)
            duration = choice([randint(120, 300), None])
            release_year = choice([randint(1990, 2023), None])
            genre = choice(genres)
            file_url = choice(file_urls)
            cover_url = choice(cover_urls)
            is_active = choice([True, False])
            created_at = datetime.now()
            updated_at = datetime.now()

            song_data = {
                "title": title,
                "artist": artist,
                "duration": duration,
                "release_year": release_year,
                "genre": genre,
                "file_url": file_url,
                "cover_url": cover_url,
                "is_active": is_active,
                "created_at": created_at,
                "updated_at": updated_at,
            }
            song_records.append(song_data)

            playlist_name = choice(playlist_names)
            description = choice([None, f"Description of {playlist_name}"])
            playlist_data = {
                "name": playlist_name,
                "description": description,
                "created_at": created_at,
                "updated_at": updated_at,
            }
            playlist_records.append(playlist_data)

            playlist = Playlist(**playlist_data)
            song = Song(**song_data)

            song.playlist = playlist

            session.add(playlist)  
            session.add(song)    

            if len(song_records) % 10000 == 0:
                session.commit()

        session.commit()

   


if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)

    # songs_df, playlists_df = create_data_and_save_to_db()
    # songs_df, playlists_df = preprocess_data(songs_df, playlists_df)
    songs_df, playlists_df = retrieve_data_from_db()
    print(songs_df.head())
    print(playlists_df.head())
    # concat_df=get_data_for_csv_concat()
    # print(concat_df)

    # print(songs_df.shape)
    # print(playlists_df.shape())
    # print(songs_df.describe())
    # print(playlists_df.describe())