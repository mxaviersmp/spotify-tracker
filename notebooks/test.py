import asyncio

from app.spotify.tasks import get_played_tracks


async def main():
    # async with db:
    #     # query = {'email': 'matheus.sampaio011@gmail.com'}
    #     resp = await User.objects.all()
    #     print(resp)
    # return
    # print(await update_access_tokens())
    print(await get_played_tracks())


asyncio.run(main())
