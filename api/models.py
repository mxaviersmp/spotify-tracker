from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class UserModel(BaseModel):
    id: str
    display_name: str
    email: str
    country: str
    uri: str
    href: str


class UserRefreshToken(UserModel):
    refresh_token: str


class UserPassword(UserRefreshToken):
    password: str


class UserInDB(UserRefreshToken):
    hashed_password: str


class TrackModel(BaseModel):
    id: str
    name: Optional[str]
    href: Optional[str]
    popularity: Optional[int]
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
    id: str
    name: Optional[str]
    href: Optional[str]
    popularity: Optional[int]
    genres: Optional[str]


class PlayedTrackModel(BaseModel):
    id: int
    user: Dict = {'id': 'string'}
    track: TrackModel
    artist: ArtistModel
    played_at: datetime
