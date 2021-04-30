from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_env: Optional[str] = ''
    client_id: Optional[str] = ''
    client_secret: Optional[str] = ''
    oauth_authorize_url: Optional[str] = ''
    oauth_token_url: Optional[str] = ''
    redirect_uri: Optional[str] = ''
    scope: Optional[str] = ''
    b64_client: Optional[str] = ''
    secret_key: Optional[str] = ''
    algorithm: Optional[str] = ''
    access_token_expire_minutes: Optional[int] = 0


SETTINGS = Settings()

AUDIO_FEATURES = [
    'popularity',
    'danceability',
    'energy',
    'loudness',
    'speechiness',
    'acousticness',
    'inOptional[str] = ''umentalness',
    'liveness',
    'valence',
    'tempo',
    'key',
    'mode',
    'duration_ms',
    'time_signature',
]
