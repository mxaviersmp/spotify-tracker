from ormar.exceptions import NoMatch

from app.database.schema import User, UserToken


async def get_user(query):
    """Gets user from database."""
    try:
        user = await User.objects.get(**query)
        return user
    except NoMatch:
        return None


async def create_user(user):
    """Create new user on database."""
    user = await User.objects.create(**user)
    await UserToken.objects.create(user=user)
    return user
