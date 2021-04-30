from typing import Dict, List, Text, Union

from app.database.schema import User, UserToken


async def get_all_users():
    """Gets all users from db."""
    return await User.objects.all()


async def update_user(user: User):
    """Updates user on db."""
    user = await user.update()
    await UserToken.objects.create(user=user)


async def add_scopes(query: Dict, scopes: Union[List[Text], Text]):
    """Add scopes to user on db."""
    if not isinstance(scopes, list):
        scopes = [scopes]
    user = await User.objects.get_or_none(**query)
    if user:
        user_scopes = user.scopes
        user_scopes = set(user_scopes.split())
        _ = [user_scopes.add(scope) for scope in scopes]
        user.scopes = ' '.join(user_scopes)
        user = await user.update()
    return user


async def remove_scopes(query: Dict, scopes: Union[List[Text], Text]):
    """Removes scopes from user on db."""
    if not isinstance(scopes, list):
        scopes = [scopes]
    user = await User.objects.get_or_none(**query)
    if user:
        user_scopes = user.scopes
        user_scopes = set(user_scopes.split())
        _ = [user_scopes.remove(scope) for scope in scopes]
        user.scopes = ' '.join(user_scopes)
        user = await user.update()
    return user
