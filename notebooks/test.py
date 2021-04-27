import asyncio
import json

from rich import print

from app.database.schema import (  # TrackArtist,
    Artist,
    Genre,
    PlayedTrack,
    Track,
    TrackArtist,
    User,
    UserToken,
    db,
)


async def add_users():
    async with db:
        with open('users.json~') as f:
            users = json.load(f)
        await User.objects.bulk_create(
            [User(**u) for u in users]
        )
        await UserToken.objects.bulk_create(
            [UserToken(user=u.get('id')) for u in users]
        )
    return


async def main():
    async with db:
        query = {'id': 'flycher'}
        resp = await User.objects.get(**query)
        resp.scopes = 'admin user items'
        await resp.update()
        print(resp)
    return


asyncio.run(main())
