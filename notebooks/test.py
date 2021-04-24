import asyncio

from rich import print

import sptf

r = asyncio.run(sptf.spotify_db.select_table('users', 'id'))
print(r)
asyncio.run(sptf.spotify_db.insert_table(
    'user_token', ['user_id'],
    [{'user_id': 'flycher'}, {'user_id': '4di24l3yf9cxgtob8xsa1fkkk'}]
))
r = asyncio.run(sptf.spotify_db.select_table('user_token', '*'))
print(r)
