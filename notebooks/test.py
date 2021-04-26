import asyncio

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


async def main():
    async with db:
        response = await User.objects.all()
        print(response[1].json())
    return


asyncio.run(main())
