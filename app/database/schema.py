import os
from datetime import datetime
from typing import Optional

import databases
import ormar
import sqlalchemy

DB_CONNECTOR = os.getenv('DB_CONNECTOR')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_DATABASE = os.getenv('DB_DATABASE')

DB_URL = f'{DB_CONNECTOR}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'

db = databases.Database(DB_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    """Base table metadata."""

    metadata = metadata
    database = db


class User(ormar.Model):
    """
    `users` table mapping.

    Attributes
    ----------
        id: str, primary key
        display_name: str
        href: str
        email: str
        country: str
        uri: str
        refresh_token: str
        hashed_password: str
        scopes: str
    """

    class Meta(BaseMeta):
        tablename = 'users'

    id: str = ormar.Text(primary_key=True)
    email: str = ormar.Text(unique=True)
    display_name: str = ormar.Text()
    href: str = ormar.Text()
    country: str = ormar.Text()
    uri: str = ormar.Text()
    refresh_token: str = ormar.Text()
    hashed_password: str = ormar.Text()
    scopes: str = ormar.Text()


class UserToken(ormar.Model):
    """
    `user_tokens` table mapping.

    Attributes
    ----------
        id: int, primary key
        user: User, foreign key
        access_token: str
    """

    class Meta(BaseMeta):
        tablename = 'user_tokens'

    id: str = ormar.Integer(primary_key=True, autoincrement=True)
    user: User = ormar.ForeignKey(User)
    access_token: Optional[str] = ormar.Text(nullable=True)


class Track(ormar.Model):
    """
    `tracks` table mapping.

    Attributes
    ----------
        id: str, primary key
        name: str
        href: str
        popularity: int, optional
        danceability: float, optional
        energy: float, optional
        loudness: float, optional
        speechiness: float, optional
        acousticness: float, optional
        instrumentalness: float, optional
        liveness: float, optional
        valence: float, optional
        tempo: float, optional
        key: int, optional
        mode: int, optional
        duration_ms: int, optional
        time_signature: int, optional
    """

    class Meta(BaseMeta):
        tablename = 'tracks'

    id: str = ormar.Text(primary_key=True)
    name: str = ormar.Text()
    href: str = ormar.Text()
    uri: str = ormar.Text()
    popularity: int = ormar.Integer()
    danceability: float = ormar.Float(nullable=True)
    energy: float = ormar.Float(nullable=True)
    loudness: float = ormar.Float(nullable=True)
    speechiness: float = ormar.Float(nullable=True)
    acousticness: float = ormar.Float(nullable=True)
    instrumentalness: float = ormar.Float(nullable=True)
    liveness: float = ormar.Float(nullable=True)
    valence: float = ormar.Float(nullable=True)
    tempo: float = ormar.Float(nullable=True)
    key: int = ormar.Integer(nullable=True)
    mode: int = ormar.Integer(nullable=True)
    duration_ms: int = ormar.Integer(nullable=True)
    time_signature: int = ormar.Integer(nullable=True)


class Artist(ormar.Model):
    """
    `artists` table mapping.

    Attributes
    ----------
        id: str, primary key
        name: str
        href: str
        popularity: int, optional
    """

    class Meta(BaseMeta):
        tablename = 'artists'

    id: str = ormar.Text(primary_key=True)
    name: str = ormar.Text()
    href: str = ormar.Text()
    uri: str = ormar.Text()
    popularity: int = ormar.Integer(nullable=True)


class Genre(ormar.Model):
    """
    `genres` table mapping.

    Attributes
    ----------
        id: str, primary key
        artist: Artist, foreign key
        genre: str
    """

    class Meta(BaseMeta):
        tablename = 'genres'

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    artist: Artist = ormar.ForeignKey(Artist)
    genre: str = ormar.Text()


class TrackArtist(ormar.Model):
    """
    `tracks_artists` table mapping.

    Attributes
    ----------
        id: str, primary key
        artist: Artist, foreign key
        track: Track, foreign key
    """

    class Meta(BaseMeta):
        tablename = 'tracks_artists'

    id: str = ormar.Integer(primary_key=True, autoincrement=True)
    artist: Artist = ormar.ForeignKey(Artist)
    track: Track = ormar.ForeignKey(Track)


class PlayedTrack(ormar.Model):
    """
    `played_tracks` table mapping.

    Attributes
    ----------
        id: str, primary key
        user: User, foreign key
        track: Track, foreign key
        played_at: datetime
    """

    class Meta(BaseMeta):
        tablename = 'played_tracks'

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    user: User = ormar.ForeignKey(User)
    track: Track = ormar.ForeignKey(Track)
    played_at: datetime = ormar.DateTime()


if __name__ == '__main__':
    # create the database
    # note that in production you should use migrations
    # note that this is not required if you connect to existing database
    engine = sqlalchemy.create_engine(DB_URL)
    # just to be sure we clear the db before
    metadata.drop_all(engine)
    metadata.create_all(engine)
