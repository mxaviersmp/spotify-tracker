from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies.security import get_current_user
from app.api.models import PlayedTrackModel, UserModel
from app.database.schema import PlayedTrack

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/me', response_model=UserModel)
async def me(current_user: UserModel = Depends(get_current_user)):  # noqa:B008
    """User information."""
    return current_user


@router.get('/played-tracks', response_model=List[PlayedTrackModel])
async def played_tracks(current_user: UserModel = Depends(get_current_user)):  # noqa:B008
    """User played tracks."""
    played_tracks = await PlayedTrack.objects.select_related(
        ['track']
    ).all(user=current_user.id)
    return played_tracks
