import asyncio
import json
from typing import Counter

from rich import print

from app.api.models import TrackModel
from app.database.schema import (  # TrackArtist,
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
        with open('users.json') as f:
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
        query = {'user': 'flycher'}
        played_tracks = await PlayedTrack.objects.all(**query)
        tracks = await Track.objects.select_related(
            ['trackartists']
        ).all(id__in=[r.track.id for r in played_tracks])
        for t in tracks:
            for ta in t.trackartists:
                await ta.artist.load()
        count_tracks = Counter([pt.track.id for pt in played_tracks])
        print(TrackModel(**tracks[0].dict()).dict())
    return


asyncio.run(main())
