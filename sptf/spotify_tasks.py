import asyncio
import datetime

import dateutil.parser

import sptf.spotify_api as api
from sptf.spotify_db import Artist, PlayedTrack, Track, UserToken, db
from sptf.utils.data import rename_dict_keys, select_dict_keys


async def update_access_tokens():
    """Fetches new access_tokens."""
    async with db:
        tokens = await UserToken.objects.select_related('user').all()
        for token in tokens:
            token.access_token = api.get_access_token(
                token.user.refresh_token
            )
        await UserToken.objects.bulk_update(tokens)


async def get_played_tracks():
    """Fetches users played tracks from the last day and updates tables."""
    async with db:
        tokens = await UserToken.objects.all()
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=30)
        yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
        all_tracks = []
        for token in tokens:
            user_tracks = api.get_recently_played(
                token.access_token, after_timestamp=yesterday_unix_timestamp
            )
            for track in user_tracks:
                track['user_id'] = token.user.id
                track['artist_id'] = track.get('track').get('artists')[0].get('id')
                track['track_id'] = track.get('track').get('id')
            all_tracks.append(user_tracks)
        all_tracks = sum(all_tracks, [])

    await save_new_tracks(all_tracks)
    await save_new_artists(all_tracks)
    await save_played_tracks(all_tracks)


async def save_new_tracks(all_tracks):
    """Saves new tracks."""
    async with db:
        new_tracks = [track.get('track') for track in all_tracks]
        new_tracks = select_dict_keys(new_tracks, ['id', 'name', 'href', 'popularity'])

        existing_tracks = await Track.objects.fields(
            ['id', 'name', 'href', 'popularity']
        ).all()
        existing_tracks = [track.id for track in existing_tracks]

        new_tracks = [*filter(
            lambda x: x.get('id') not in existing_tracks, new_tracks
        )]
        await Track.objects.bulk_create([
            Track(**track) for track in new_tracks
        ])


async def save_new_artists(all_tracks):
    """Saves new user artists."""
    async with db:
        new_artists = [track.get('track').get('artists')[0] for track in all_tracks]
        new_artists = select_dict_keys(new_artists, ['id', 'name', 'href'])

        existing_artists = await Artist.objects.fields(
            ['id', 'name', 'href']
        ).all()
        existing_artists = [artist.id for artist in existing_artists]

        new_artists = [*filter(
            lambda x: x.get('id') not in existing_artists, new_artists
        )]
        await Artist.objects.bulk_create([
            Artist(**artist) for artist in new_artists
        ])


async def save_played_tracks(all_tracks):
    """Saves new user recently played tracks."""
    async with db:
        played_tracks = select_dict_keys(
            all_tracks,
            ['played_at', 'user_id', 'artist_id', 'track_id']
        )
        played_tracks = rename_dict_keys(
            played_tracks,
            {'user_id': 'user', 'artist_id': 'artist', 'track_id': 'track'}
        )

        for track in played_tracks:
            played_at = track.get('played_at')
            track['played_at'] = dateutil.parser.parse(played_at).replace(tzinfo=None)
        await PlayedTrack.objects.bulk_create([
            PlayedTrack(**track) for track in played_tracks
        ])


async def get_track_info():
    """Fetches information for new tracks."""
    async with db:
        new_tracks = await Track.objects.all(duration_ms=None)
        new_tracks_id = [track.id for track in new_tracks]

        access_tokens = await UserToken.objects.all()
        access_tokens = [token.access_token for token in access_tokens]

        audio_features = api.get_audio_features(access_tokens, new_tracks_id)
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

        new_tracks.sort(key=lambda x: x.id)
        audio_features.sort(key=lambda x: x.get('id'))
        await Track.objects.bulk_update(
            [track.update_from_dict(features)
             for track, features in zip(new_tracks, audio_features)]
        )


async def get_artist_info():
    """Fetches information for new artists."""
    async with db:
        new_artists = await Artist.objects.all(popularity=None)
        new_artists_id = [artist.id for artist in new_artists]

        access_tokens = await UserToken.objects.all()
        access_tokens = [token.access_token for token in access_tokens]

        artists_info = api.get_artists(access_tokens, new_artists_id)
        artists_info = select_dict_keys(artists_info, ['id', 'popularity', 'genres'])
        for artist in artists_info:
            artist['genres'] = ','.join(artist.get('genres'))

        new_artists.sort(key=lambda x: x.id)
        artists_info.sort(key=lambda x: x.get('id'))
        await Artist.objects.bulk_update(
            [artist.update_from_dict(info)
             for artist, info in zip(new_artists, artists_info)]
        )


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
