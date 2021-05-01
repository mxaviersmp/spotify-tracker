import datetime

import dateutil.parser

from app.database.schema import (
    Artist,
    Genre,
    PlayedTrack,
    Track,
    TrackArtist,
    UserToken,
    db,
)
from app.spotify.api import (
    get_access_token,
    get_artists,
    get_audio_features,
    get_recently_played,
)
from app.utils.data import (
    filter_duplicate_dicts_by_key,
    rename_dict_keys,
    select_dict_keys,
)


async def update_access_tokens():
    """
    Fetches new access_tokens for all users.

    Gets `users.refresh_token` and updates `user_tokens`.
    """
    async with db:
        tokens = await UserToken.objects.select_related('user').all()
        for token in tokens:
            token.access_token = await get_access_token(
                token.user.refresh_token
            )
        await UserToken.objects.bulk_update(tokens)


async def get_played_tracks():
    """
    Fetches users played tracks from the last day, adds new artists and new tracks.

    Gets `users.access_token` to fetch new user tracks.
    Filters tracks and artists not on the database to add to `tracks` and `artists`.
    Adds all new played tracks to `played_tracks`.
    """
    async with db:
        tokens = await UserToken.objects.all()
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
        all_tracks = []
        for token in tokens:
            user_tracks = await get_recently_played(
                token.access_token, after_timestamp=yesterday_unix_timestamp
            )
            for track in user_tracks:
                track['user_id'] = token.user.id
                track['artist_id'] = track.get('track').get('artists')[0].get('id')
                track['track_id'] = track.get('track').get('id')
            all_tracks.append(user_tracks)
        all_tracks = sum(all_tracks, [])

    await save_new_artists(all_tracks)
    await save_new_tracks(all_tracks)
    await save_played_tracks(all_tracks)


async def save_new_artists(all_tracks):
    """
    Saves new user artists.

    Filter artists not on `artists`. Save artists to `artists`.
    """
    async with db:
        new_artists = [track.get('track').get('artists') for track in all_tracks]
        new_artists = sum(new_artists, [])
        new_artists = select_dict_keys(new_artists, ['id', 'name', 'href', 'uri'])

        existing_artists = await Artist.objects.fields(
            ['id', 'name', 'href', 'uri']
        ).all()
        existing_artists = [artist.id for artist in existing_artists]

        new_artists = [*filter(
            lambda x: x.get('id') not in existing_artists, new_artists
        )]
        new_artists = filter_duplicate_dicts_by_key(new_artists, 'id')

        await Artist.objects.bulk_create([
            Artist(**artist) for artist in new_artists
        ])


async def save_new_tracks(all_tracks):
    """
    Saves new tracks.

    Filter tracks not on `tracks`. Extract artists from the tracks.
    Save tracks to `tracks` and link to artists on `tracks_artists`.
    """
    async with db:
        new_tracks = [track.get('track') for track in all_tracks]

        existing_tracks = await Track.objects.fields(
            ['id', 'name', 'href', 'uri', 'popularity']
        ).all()
        existing_tracks = [track.id for track in existing_tracks]

        new_tracks = [*filter(
            lambda x: x.get('id') not in existing_tracks, new_tracks
        )]
        new_tracks_artists = [
            {'track': track.get('id'), 'artist': artist.get('id')}
            for track in new_tracks for artist in track.get('artists')
        ]
        new_tracks = select_dict_keys(
            new_tracks,
            ['id', 'name', 'href', 'uri', 'popularity']
        )
        new_tracks = filter_duplicate_dicts_by_key(new_tracks, 'id')

        await Track.objects.bulk_create([
            Track(**track) for track in new_tracks
        ])
        await TrackArtist.objects.bulk_create([
            TrackArtist(**track_artist) for track_artist in new_tracks_artists
        ])


async def save_played_tracks(all_tracks):
    """
    Saves new user recently played tracks.

    Saves all new played tracks to `played_tracks`.
    """
    async with db:
        played_tracks = select_dict_keys(
            all_tracks,
            ['played_at', 'user_id', 'track_id']
        )
        played_tracks = rename_dict_keys(
            played_tracks,
            {'user_id': 'user', 'track_id': 'track'}
        )

        for track in played_tracks:
            played_at = track.get('played_at')
            track['played_at'] = dateutil.parser.parse(played_at).replace(tzinfo=None)
        await PlayedTrack.objects.bulk_create([
            PlayedTrack(**track) for track in played_tracks
        ])


async def get_track_info():
    """
    Fetches information for new tracks.

    Gets tracks from `tracks` without audio features.
    Updates tracks with audio features.
    """
    async with db:
        new_tracks = await Track.objects.all(duration_ms=None)
        new_tracks_id = [track.id for track in new_tracks]

        access_tokens = await UserToken.objects.all()
        access_tokens = [token.access_token for token in access_tokens]

        audio_features = await get_audio_features(access_tokens, new_tracks_id)
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
    """
    Fetches information for new artists.

    Gets artists from `artists` without information.
    Extracts genres for artists.
    Updates artists with information.
    Link artists to genres on `genres`.
    """
    async with db:
        new_artists = await Artist.objects.all(popularity=None)
        new_artists_id = [artist.id for artist in new_artists]

        access_tokens = await UserToken.objects.all()
        access_tokens = [token.access_token for token in access_tokens]

        artists_info = await get_artists(access_tokens, new_artists_id)
        artists_info = select_dict_keys(artists_info, ['id', 'popularity', 'genres'])
        genres = []
        for artist in artists_info:
            artist_genres = artist.pop('genres')
            for genre in artist_genres:
                genres.append({'genre': genre, 'artist': artist.get('id')})

        new_artists.sort(key=lambda x: x.id)
        artists_info.sort(key=lambda x: x.get('id'))
        await Artist.objects.bulk_update(
            [artist.update_from_dict(info)
             for artist, info in zip(new_artists, artists_info)]
        )
        await Genre.objects.bulk_create([
            Genre(**genre) for genre in genres
        ])
