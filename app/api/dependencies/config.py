from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    client_id: str
    client_secret: str
    oauth_authorize_url: str
    oauth_token_url: str
    redirect_uri: str
    scope: str
    b64_client: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


SETTINGS = Settings()

AUDIO_FEATURES = [
    'popularity',
    'danceability',
    'energy',
    'loudness',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'liveness',
    'valence',
    'tempo',
    'key',
    'mode',
    'duration_ms',
    'time_signature',
]
