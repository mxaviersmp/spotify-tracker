from typing import List

from fastapi import APIRouter, Security

from app.api.crud.played_tracks import get_played_tracks
from app.api.dependencies.security import get_current_user
from app.api.models import PlayedTrackModel, UserModel

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
    current_user: UserModel = Security(get_current_user, scopes=['user'])  # noqa:B008
):
    """User played tracks."""
    played_tracks = await get_played_tracks({'user': current_user.id})
    return played_tracks
