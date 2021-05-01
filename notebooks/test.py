import asyncio

from app.database.db import db
from app.database.schema import Artist


async def main():
    async with db:
        # query = {'email': 'matheus.sampaio011@gmail.com'}
        resp = await Artist.objects.select_.all()
        print([r.dict().get('trackartists') for r in resp])
    # return

asyncio.run(main())
