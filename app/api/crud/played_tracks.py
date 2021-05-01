from collections import Counter, defaultdict
from typing import DefaultDict, Dict, List, Optional

from app.database.schema import PlayedTrack, Track, TrackArtist
from app.utils.data import filter_duplicate_dicts_by_key


async def get_played_tracks(query: Dict) -> List[Dict]:
    """Gets user from database."""
    played_tracks = await PlayedTrack.objects.select_related(
        ['track']
    ).all(**query)
    return [pt.dict() for pt in played_tracks]


async def get_tracks(query: Optional[Dict] = None) -> List[Dict]:
    """Gets user listened tracks."""
    if query is None:
        query = dict()
    played_tracks = await PlayedTrack.objects.all(**query)
    tracks = await Track.objects.select_related(
        ['trackartists']
    ).all(id__in=[r.track.id for r in played_tracks])
    for t in tracks:
        for ta in t.trackartists:
            await ta.artist.load()
    count_tracks = Counter([pt.track.id for pt in played_tracks])

    tracks = [t.dict() for t in tracks]
    tracks = filter_duplicate_dicts_by_key(tracks, 'id')
    return [{**t, 'count': count_tracks[t['id']]} for t in tracks]


async def get_artists(query: Optional[Dict] = None) -> List[Dict]:
    """Gets user listened artists."""
    if query is None:
        query = dict()
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

    artists = [a.dict() for a in artists]
    artists = filter_duplicate_dicts_by_key(artists, 'id')
    return [{**a, 'count': count_artists[a['id']]} for a in artists]


async def get_audio_features(
    query: Optional[Dict] = None, features: Optional[List[str]] = None
) -> DefaultDict:
    """Gets user listened audio features."""
    if query is None:
        query = dict()
    if features is None:
        features = list()
    played_tracks = await PlayedTrack.objects.select_related('track').all(**query)
    audio_features = defaultdict(list)
    for pt in played_tracks:
        pt_dict = pt.track.dict()
        [audio_features[k].append(pt_dict.get(k)) for k in features]
    return audio_features


async def get_genres(query: Optional[Dict] = None) -> List[Dict]:
    """Gets user listened genres."""
    if query is None:
        query = dict()
    played_tracks = await PlayedTrack.objects.select_related(
        ['track__trackartists']
    ).all(**query)
    track_artists = await TrackArtist.objects.select_related(
        ['artist__genres']
    ).all(track__id__in=[pt.track.id for pt in played_tracks])
    artists = [ta.artist for ta in track_artists]
    count_genres = Counter(
        [g.genre for artist in artists for g in artist.genres]
    )
    return count_genres
