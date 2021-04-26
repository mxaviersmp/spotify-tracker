from collections import Counter
from typing import Dict, List

from app.database.schema import PlayedTrack, Track, TrackArtist


async def get_played_tracks(query: Dict) -> List[Dict]:
    """Gets user from database."""
    played_tracks = await PlayedTrack.objects.select_related(
        ['track']
    ).all(**query)
    return [pt.dict() for pt in played_tracks]


async def get_tracks(query: Dict) -> List[Dict]:
    """Gets user listened tracks."""
    played_tracks = await PlayedTrack.objects.all(**query)
    tracks = await Track.objects.select_related(
        ['trackartists']
    ).all(id__in=[r.track.id for r in played_tracks])
    for t in tracks:
        for ta in t.trackartists:
            await ta.artist.load()
    count_tracks = Counter([pt.track.id for pt in played_tracks])
    return [{**t.dict(), 'count': count_tracks[t.id]} for t in tracks]


async def get_artists(query: Dict) -> List[Dict]:
    """Gets user listened artists."""
    played_tracks = await PlayedTrack.objects.select_related(
        ['track__trackartists']
    ).all(**query)
    track_artists = await TrackArtist.objects.select_related(
        ['artist__genres']
    ).all(track__id__in=[pt.track.id for pt in played_tracks])
    artists = [ta.artist for ta in track_artists]
    count_artists = Counter(
        [ta.artist.id for pt in played_tracks for ta in pt.track.trackartists]
    )
    return [{**a.dict(), 'count': count_artists[a.id]} for a in artists]


async def get_audio_features(query: Dict) -> List[Dict]:
    """Gets user listened audio features."""


async def get_genres(query: Dict) -> List[Dict]:
    """Gets user listened genres."""
