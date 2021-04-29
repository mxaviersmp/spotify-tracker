# from pathlib import Path
# from app.etl.tasks import update_access_tokens
# import asyncio
# import json

# from rich import print

# from app.database.schema import (  # TrackArtist,
#     Artist,
#     Genre,
#     PlayedTrack,
#     Track,
#     TrackArtist,
#     User,
#     UserToken,
#     db,
# )


# async def add_users():
#     async with db:
#         with open(Path(__file__).resolve().parent / 'users.json~') as f:
#             users = json.load(f)
#         await User.objects.bulk_create(
#             [User(**u) for u in users]
#         )
#         await UserToken.objects.bulk_create(
#             [UserToken(user=u.get('id')) for u in users]
#         )
#     return


# async def main():
#     await update_access_tokens()
#     # async with db:
#     #     query = {'id': 'flycher'}
#     #     resp = await User.objects.get(**query)
#     #     print(resp)
#     return


# asyncio.run(main())

from app.api.main import app_version

print(app_version)
