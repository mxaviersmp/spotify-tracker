import asyncio
import json
from pathlib import Path

from rich import print

from app.database.schema import (
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
        with open(Path(__file__).resolve().parent / 'users.json~') as f:
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
        # query = {'email': 'matheus.sampaio011@gmail.com'}
        resp = await User.objects.all()
        print(resp)
    return


asyncio.run(main())
