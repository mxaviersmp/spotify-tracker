import asyncio

from app.database.db import db
from app.database.schema import Track


async def main():
    async with db:
        # query = {'email': 'matheus.sampaio011@gmail.com'}
        resp = await Track.objects.all()
        print(resp)
    # return
    # print(await update_access_tokens())
    # print(await get_played_tracks())


asyncio.run(main())
