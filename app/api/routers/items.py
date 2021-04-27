from typing import Dict, List, Union

from fastapi import APIRouter, Query, Security

from app.api.crud.played_tracks import (
    get_artists,
    get_audio_features,
    get_genres,
    get_tracks,
)
from app.api.dependencies.config import AUDIO_FEATURES
from app.api.dependencies.security import get_current_user
from app.api.models import ArtistModel, TrackModel, UserModel

router = APIRouter(
    prefix='/items',
    tags=['items'],
)


@router.get('/tracks', response_model=List[TrackModel])
async def tracks(
    current_user: UserModel = Security(get_current_user, scopes=['items'])  # noqa:B008
):
    """User played tracks."""
    return await get_tracks()


@router.get('/artists', response_model=List[ArtistModel])
async def artists(
    current_user: UserModel = Security(get_current_user, scopes=['items'])  # noqa:B008
):
    """User played artists."""
    return await get_artists()


@router.get('/audio-features', response_model=Dict[str, List[Union[float, int]]])
async def audio_features(
    features: List[str] = Query(  # noqa: B008
        AUDIO_FEATURES,
        description='List of features to get. Accepted values in default'
    ),
    current_user: UserModel = Security(get_current_user, scopes=['items'])  # noqa:B008
):
    """User played tracks audio features."""
    features = [*(set(AUDIO_FEATURES) & set(features))]
    return await get_audio_features(features=features)


@router.get('/genres', response_model=Dict[str, int])
async def genres(
    current_user: UserModel = Security(get_current_user, scopes=['items'])  # noqa:B008
):
    """User played tracks artists genres."""
    return await get_genres()
