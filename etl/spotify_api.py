import os
import random

import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

B64_CLIENT = os.getenv('B64_CLIENT')


def get_access_token(refresh_token):
    """
    Gets a new access token using the refresh token.

    Parameters
    ----------
    refresh_token : str
        spotify user refresh token

    Returns
    -------
    str
        spotify user access token
    """
    oauth_token_url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {
        'Authorization': f'Basic {B64_CLIENT}'
    }
    response = requests.post(
        oauth_token_url,
        data=payload,
        headers=headers,
    )
    token = response.json()
    return token.get('access_token')


def get_recently_played(access_token, after_timestamp, limit=50):
    """
    Gets the user most recently played music since `after_timestamp`.

    Parameters
    ----------
    access_token : str
        spotify user access token
    after_timestamp : int
        unix timestamp
    limit : int, optional
        maximum number tracks per requests, by default 50

    Returns
    -------
    list of dict
        list with the users tracks
    """
    tracks = []
    url = 'https://api.spotify.com/v1/me/player/recently-played?limit={}&after={}'.format(
        limit, after_timestamp
    )
    while url:
        response = requests.get(
            url,
            headers={'Authorization': f'Bearer {access_token}'}
        )
        resp_json = response.json()
        tracks.append(resp_json.get('items') or [])
        url = resp_json.get('next')
    tracks = sum(tracks, [])
    return tracks


def get_audio_features(access_tokens, track_ids, limit=100):
    """
    Gets the audio features from the `track_ids`.

    Parameters
    ----------
    access_tokens : list of str
        spotify access token
    track_ids : list of str
        list of track ids
    limit : int, optional
        maximum number of tracks per request, by default 100

    Returns
    -------
    list of dict
        list with the tracks audio features
    """
    tracks = []
    size = len(track_ids)
    url = 'https://api.spotify.com/v1/audio-features?ids={}'
    for i in range(0, size, limit):
        current_tracks = ','.join(track_ids[i: i + limit])
        access_token = random.choice(access_tokens)
        response = requests.get(
            url.format(current_tracks),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        resp_json = response.json()
        audio_features = resp_json.get('audio_features')
        if audio_features:
            tracks.append(audio_features)
    tracks = sum(tracks, [])
    return tracks


def get_artists(access_tokens, artist_ids, limit=100):
    """
    Gets the artists info from the `artist_ids`.

    Parameters
    ----------
    access_tokens : list of str
        spotify access token
    artist_ids : list of str
        list of track ids
    limit : int, optional
        maximum number of tracks per request, by default 100

    Returns
    -------
    list of dict
        list with the artists info
    """
    artists = []
    size = len(artist_ids)
    url = 'https://api.spotify.com/v1/artists?ids={}'
    for i in range(0, size, limit):
        current_artists = ','.join(artist_ids[i: i + limit])
        access_token = random.choice(access_tokens)
        response = requests.get(
            url.format(current_artists),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        resp_json = response.json()
        artists_info = resp_json.get('artists')
        if artists_info:
            artists.append(artists_info)
    artists = sum(artists, [])
    return artists
