from datetime import datetime
from typing import Optional

import ormar

from app.database.db import db, metadata


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
        pass

    id: str = ormar.Text(primary_key=True)
    email: str = ormar.Text(unique=True)
    display_name: str = ormar.Text(nullable=True)
    href: str = ormar.Text(nullable=True)
    country: str = ormar.Text(nullable=True)
    uri: str = ormar.Text(nullable=True)
    refresh_token: str = ormar.Text(nullable=True)
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
        pass

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
        pass

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
        pass

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
        pass

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
        pass

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
        pass

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    user: User = ormar.ForeignKey(User)
    track: Track = ormar.ForeignKey(Track)
    played_at: datetime = ormar.DateTime()
