from typing import Dict, Optional

from asyncpg.exceptions import UniqueViolationError

from app.database.schema import User, UserToken


async def get_user(query: Dict) -> Optional[User]:
    """Gets user from database."""
    user = await User.objects.get_or_none(**query)
    return user


async def create_user(user) -> Optional[User]:
    """Create new user on database."""
    try:
        user = await User.objects.create(**user)
        await UserToken.objects.create(user=user)
        return user
    except UniqueViolationError:
        return None
