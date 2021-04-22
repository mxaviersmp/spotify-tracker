import asyncio
import datetime

import dateutil.parser

import sptf.spotify_api as api
import sptf.spotify_db as db


def select_dict_keys(dict_list, keys):
    """Returns subset of dictionary."""
    return [{k: d.get(k) for k in keys} for d in dict_list]


async def update_access_tokens():
    """Fetches new access_tokens."""
    tokens = await db.select_table(
        'users', ['id', 'refresh_token']
    )
    for token in tokens:
        token['access_token'] = api.get_access_token(
            token.get('refresh_token')
        )
    tokens = select_dict_keys(tokens, ['id', 'access_token'])
    table = 'user_token'
    columns = ['access_token']
    key = 'id'
    await db.update_table(table, columns, key, tokens)


async def get_played_tracks():
    """Fetches users played tracks from the last day and updates tables."""
    tokens = await db.select_table(
        'user_token', ['id', 'access_token']
    )
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=30)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    all_tracks = []
    for token in tokens:
        user_tracks = api.get_recently_played(
            token.get('access_token'), after_timestamp=yesterday_unix_timestamp
        )
        for track in user_tracks:
            track['user_id'] = token.get('id')
            track['artist_id'] = track.get('track').get('artists')[0].get('id')
            track['track_id'] = track.get('track').get('id')
        all_tracks.append(user_tracks)
    all_tracks = sum(all_tracks, [])

    await save_new_tracks(all_tracks)
    await save_new_artists(all_tracks)
    await save_user_tracks(all_tracks)


async def save_user_tracks(all_tracks):
    """Saves new user recently played tracks."""
    played_tracks = select_dict_keys(
        all_tracks,
        ['played_at', 'user_id', 'artist_id', 'track_id']
    )
    for track in played_tracks:
        played_at = track.get('played_at')
        track['played_at'] = dateutil.parser.parse(played_at).replace(tzinfo=None)
    await db.insert_table(
        'played_tracks',
        ['played_at', 'user_id', 'artist_id', 'track_id'],
        played_tracks
    )


async def save_new_tracks(all_tracks):
    """Saves new tracks."""
    new_tracks = [track.get('track') for track in all_tracks]
    new_tracks = select_dict_keys(new_tracks, ['id', 'name', 'href', 'popularity'])

    existing_tracks = await db.select_table(
        'tracks', 'id'
    )
    existing_tracks = [track.get('id') for track in existing_tracks]

    new_tracks = [*filter(lambda x: x.get('id') not in existing_tracks, new_tracks)]

    await db.insert_table(
        'tracks',
        ['id', 'name', 'href', 'popularity'],
        new_tracks
    )


async def save_new_artists(all_tracks):
    """Saves new user artists."""
    new_artists = [track.get('track').get('artists')[0] for track in all_tracks]
    new_artists = select_dict_keys(new_artists, ['id', 'name', 'href'])

    existing_artists = await db.select_table(
        'artists', 'id'
    )
    existing_artists = [artist.get('id') for artist in existing_artists]

    new_artists = [*filter(lambda x: x.get('id') not in existing_artists, new_artists)]

    await db.insert_table(
        'artists',
        ['id', 'name', 'href'],
        new_artists
    )


async def get_track_info():
    """Fetches information for new tracks."""
    new_tracks = await db.select_table(
        'tracks', 'id', [('duration_ms', ' IS ', 'NULL')]
    )
    new_tracks = [track.get('id') for track in new_tracks]
    access_tokens = await db.select_table(
        'user_token', 'access_token'
    )
    access_tokens = [token.get('access_token') for token in access_tokens]

    audio_features = api.get_audio_features(access_tokens, new_tracks)
    columns = [
        'danceability',
        'energy',
        'loudness',
        'speechiness',
        'acousticness',
        'instrumentalness',
        'liveness',
        'valence',
        'tempo',
        'key',
        'mode',
        'duration_ms',
        'time_signature'
    ]
    audio_features = select_dict_keys(
        audio_features,
        ['id'] + columns
    )

    table = 'tracks'
    columns = columns
    key = 'id'
    await db.update_table(table, columns, key, audio_features)


async def get_artist_info():
    """Fetches information for new artists."""
    new_artists = await db.select_table(
        'artists', 'id', [('popularity', ' IS ', 'NULL')]
    )
    new_artists = [track.get('id') for track in new_artists]
    access_tokens = await db.select_table(
        'user_token', 'access_token'
    )
    access_tokens = [token.get('access_token') for token in access_tokens]

    artists = api.get_artists(access_tokens, new_artists)
    artists = select_dict_keys(artists, ['id', 'popularity', 'genres'])

    for artist in artists:
        artist['genres'] = ','.join(artist.get('genres'))
    table = 'artists'
    columns = ['popularity', 'genres']
    key = 'id'
    await db.update_table(table, columns, key, artists)


def run_update_access_tokens():
    """Run update_access_tokens."""
    asyncio.run(update_access_tokens())


def run_get_played_tracks():
    """Run get_played_tracks."""
    asyncio.run(get_played_tracks())


def run_get_track_info():
    """Run get_track_info."""
    asyncio.run(get_track_info())


def run_get_artist_info():
    """Run get_artist_info."""
    asyncio.run(get_artist_info())
