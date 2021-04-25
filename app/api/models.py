from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


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
    """

    id: Optional[str] = None


class UserModel(BaseModel):
    """
    User model.

    Attributes
    ----------
        id: str
            user unique identifier
        display_type: str
            user nickname
        email: str
            user email
        country: str
            user country location initials
        uri: str
            user spotify uri
        href: str
            user http url
    """

    id: str
    display_name: str
    email: str
    country: str
    uri: str
    href: str


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


class UserInDB(UserRefreshToken):
    """
    UserInDB model.

    Attributes
    ----------
        hashed_password: str
            user hashed password
    """

    hashed_password: str


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
        tracks_artists: list of Artist, optional
            track artists
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

    id: str
    name: Optional[str]
    href: Optional[str]
    popularity: Optional[int]
    artists: Optional[List['ArtistModel']]
    danceability: Optional[float]
    energy: Optional[float]
    loudness: Optional[float]
    speechiness: Optional[float]
    acousticness: Optional[float]
    instrumentalness: Optional[float]
    liveness: Optional[float]
    valence: Optional[float]
    tempo: Optional[float]
    key: Optional[float]
    mode: Optional[float]
    duration_ms: Optional[float]
    time_signature: Optional[float]


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
    name: Optional[str]
    href: Optional[str]
    popularity: Optional[int]
    tracks: Optional[List['TrackModel']]
    genres: Optional[List[str]]


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


TrackModel.update_forward_refs()
ArtistModel.update_forward_refs()
