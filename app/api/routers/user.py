from datetime import date
from typing import Dict, List, Optional, Union

from fastapi import APIRouter, Query, Security

from app.api.crud.played_tracks import (
    get_artists,
    get_audio_features,
    get_genres,
    get_played_tracks,
    get_tracks,
)
from app.api.dependencies.config import AUDIO_FEATURES
from app.api.dependencies.security import get_current_user
from app.api.models import ArtistModel, PlayedTrackModel, TrackModel, UserModel

router = APIRouter(
    prefix='/user',
    tags=['user'],
)


@router.get('/me', response_model=UserModel)
async def me(
    current_user: UserModel = Security(get_current_user, scopes=['user'])  # noqa:B008
):
    """User information."""
    return current_user


@router.get('/played-tracks', response_model=List[PlayedTrackModel])
async def played_tracks(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: UserModel = Security(get_current_user, scopes=['user'])  # noqa:B008
):
    """User played tracks."""
    query = {'user': current_user.id}
    if start_date:
        query = {'played_at__gt': start_date.strftime('%Y-%m-%dT%H:%M:%S')}
    if end_date:
        query = {'played_at__lt': end_date.strftime('%Y-%m-%dT%H:%M:%S')}
    return await get_played_tracks(query)


@router.get('/tracks', response_model=List[TrackModel])
async def tracks(
    current_user: UserModel = Security(get_current_user, scopes=['user'])  # noqa:B008
):
    """User played tracks."""
    return await get_tracks({'user': current_user.id})


@router.get('/artists', response_model=List[ArtistModel])
async def artists(
    current_user: UserModel = Security(get_current_user, scopes=['user'])  # noqa:B008
):
    """User played artists."""
    return await get_artists({'user': current_user.id})


@router.get('/audio-features', response_model=Dict[str, List[Union[float, int]]])
async def audio_features(
    features: List[str] = Query(  # noqa: B008
        AUDIO_FEATURES,
        description='List of features to get. Accepted values in default'
    ),
    current_user: UserModel = Security(get_current_user, scopes=['user'])  # noqa:B008
):
    """User played tracks audio features."""
    features = [*(set(AUDIO_FEATURES) & set(features))]
    return await get_audio_features({'user': current_user.id}, features)


@router.get('/genres', response_model=Dict[str, int])
async def genres(
    current_user: UserModel = Security(get_current_user, scopes=['user'])  # noqa:B008
):
    """User played tracks artists genres."""
    return await get_genres({'user': current_user.id})
