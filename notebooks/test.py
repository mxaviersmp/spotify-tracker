import asyncio

from rich import print

from app.api.crud.played_tracks import get_artists
from app.database.db import db


async def main():
    async with db:
        # query = {'email': 'matheus.sampaio011@gmail.com'}
        resp = await get_artists()
        print(resp)
    # return

asyncio.run(main())
