from datetime import datetime
from typing import List, Optional, Text

from pydantic import BaseModel
from pydantic.class_validators import validator


class Token(BaseModel):
    """
    Token model.

    Attributes
    ----------
        access_token: str
            user access token
        token_type: str
            type of token
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    TokenData model.

    Attributes
    ----------
        id: str, optional
            user id
        scopes: list of str
            authorized scoped
    """

    id: Optional[str] = None
    scopes: List[str] = []


class UserModel(BaseModel):
    """
    User model.

    Attributes
    ----------
        id: str
            user unique identifier
        display_type: str, optional
            user nickname
        email: str
            user email
        country: str, optional
            user country location initials
        uri: str, optional
            user spotify uri
        href: str, optional
            user http url
        scopes: list of str
            user scopes
    """

    id: str
    display_name: Optional[str]
    email: str
    country: Optional[str]
    uri: Optional[str]
    href: Optional[str]
    scopes: Text


class UserRefreshToken(UserModel):
    """
    UserRefreshToken model.

    Attributes
    ----------
        refresh_token: str
            user authorize refresh token
    """

    refresh_token: str


class UserPassword(UserRefreshToken):
    """
    UserPassword model.

    Attributes
    ----------
        password: str
            user password
    """

    password: str


class TrackModel(BaseModel):
    """
    Track model.

    Attributes
    ----------
        id: str
            track unique id
        name: str, optional
            track name
        href: str, optional
            track http url
        popularity: int, optional
            track popularity in spotify
        artists: list of str, optional
            track artists names
        count: int, optional
            number of times track was played
    """

    id: str
    name: str
    href: str
    uri: str
    popularity: int
    trackartists: Optional[List[str]]
    count: Optional[int]

    @validator('trackartists', pre=True, each_item=True)
    def extract_artists_names(cls, value):  # noqa:N805
        """Extracts names of the artists from Artist."""
        return value.get('artist').get('name')


class ArtistModel(BaseModel):
    """
    Artist model.

    Attributes
    ----------
        id: str
            artist unique id
        name: str, optional
            artist name
        href: str, optional
            artist http url
        popularity: int, optional
            artist popularity
        tracks: list of TrackModel, optional
            artist tracks
        genres: list of str, optional
            artist genres
    """

    id: str
    name: str
    href: str
    uri: str
    popularity: int
    genres: Optional[List[str]]
    count: Optional[int]

    @validator('genres', pre=True, each_item=True)
    def extract_genres_names(cls, value):  # noqa:N805
        """Extracts names of the genre from Genre."""
        return value.get('genre')


class GenreModel(BaseModel):
    """
    Genre model.

    Attributes
    ----------
        id: int
            genre mapping id
        artist: Artist
            genre mapping artist
        genre: str
            genre mapping name
    """

    id = int
    artist = ArtistModel
    genre = str


class TrackArtistModel(BaseModel):
    """
    TrackArtist model.

    Attributes
    ----------
        id: int
            track artist mapping id
        artist: ArtistModel
            track artist artist
        track: TrackModel
            track artist track
    """

    id = int
    artist = ArtistModel
    track = TrackModel


class PlayedTrackModel(BaseModel):
    """
    PlayedTrack model.

    Attributes
    ----------
        id: int
            played track unique id
        user: User
            played track user
        track: str, optional
            played track
        played_at: datetime
            played track datetime
    """

    id: int
    track: TrackModel
    played_at: datetime
