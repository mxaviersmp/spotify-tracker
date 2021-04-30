from typing import List, Text

from fastapi import APIRouter, Query, Security

from app.api.crud.admin import add_scopes, get_all_users, remove_scopes
from app.api.dependencies.security import get_current_user
from app.api.models import UserModel

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
)


@router.get('/get-users', response_model=List[UserModel])
async def get_users(
    current_user: UserModel = Security(get_current_user, scopes=['admin'])  # noqa:B008
):
    """Retrieves all users."""
    return await get_all_users()


@router.get('/add-scopes', response_model=UserModel)
async def add_scopes_to_user(
    user_id: Text,
    scopes: List[str] = Query(  # noqa: B008
        [],
        description='List of scopes to add to user.'
    ),
    current_user: UserModel = Security(get_current_user, scopes=['admin'])  # noqa:B008
):
    """Adds the scopes to the user."""
    return await add_scopes({'id': user_id}, scopes)


@router.get('/remove-scopes', response_model=UserModel)
async def remove_scopes_to_user(
    user_id: Text,
    scopes: List[str] = Query(  # noqa: B008
        [],
        description='List of scopes to add to user.'
    ),
    current_user: UserModel = Security(get_current_user, scopes=['admin'])  # noqa:B008
):
    """Adds the scopes to the user."""
    return await remove_scopes({'id': user_id}, scopes)
