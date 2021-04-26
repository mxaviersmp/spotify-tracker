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
        # await User.objects.bulk_create(
        #     [User(**u) for u in users]
        # )
        # await UserToken.objects.bulk_create(
        #     [UserToken(user=u) for u in users]
        # )
        response = await User.objects.get(email='abc')
        print(response)
    return


asyncio.run(main())
