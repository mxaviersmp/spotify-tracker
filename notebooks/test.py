import asyncio

from rich import print

import sptf

r = asyncio.run(sptf.spotify_db.select_table('tracks', '*'))
print(r)
