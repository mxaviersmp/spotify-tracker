import os
import random
from typing import Dict, List, Optional, Text

from app.utils.data import select_dict_keys
from app.utils.logger import logger
from app.utils.misc import async_request

B64_CLIENT = os.getenv('B64_CLIENT')
REDIRECT_URI = os.getenv('REDIRECT_URI')
OAUTH_TOKEN_URL = os.getenv('OAUTH_TOKEN_URL')


async def get_refresh_token(code: Text) -> Dict[str, str]:
    """
    Gets a new refresh token.

    Parameters
    ----------
    code : str
        user authorization code

    Returns
    -------
    dict
        user refresh and access tokens
    """
    payload = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri' : REDIRECT_URI
    }
    headers = {
        'Authorization': f'Basic {B64_CLIENT}'
    }
    response = await async_request(
        'post',
        OAUTH_TOKEN_URL,
        data=payload,
        headers=headers,
    )
    tokens = response.json()
    tokens = select_dict_keys(tokens, ['access_token', 'refresh_token'])
    return tokens


async def get_access_token(refresh_token: Text) -> Text:
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
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {
        'Authorization': f'Basic {B64_CLIENT}'
    }
    response = await async_request(
        'post',
        OAUTH_TOKEN_URL,
        data=payload,
        headers=headers,
    )
    token = response.json()
    return token.get('access_token')


async def get_user_me(access_token: Text) -> Dict:
    """
    Gets the user information.

    Parameters
    ----------
    access_token : str
        spotify user access token

    Returns
    -------
    dict
        user information
    """
    response = await async_request(
        'get',
        'https://api.spotify.com/v1/me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    user = response.json()
    return user


async def get_recently_played(
    access_token: Text, after_timestamp: Text, limit: Optional[int] = 50
) -> List[Dict]:
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
    if not (0 < limit <= 50):
        limit = 50
        logger.warning(f'limit must be at most {limit}. setting value to {limit}')
    tracks = []
    url = 'https://api.spotify.com/v1/me/player/recently-played?limit={}&after={}'.format(
        limit, after_timestamp
    )
    while url:
        response = await async_request(
            'get',
            url,
            headers={'Authorization': f'Bearer {access_token}'}
        )
        resp_json = response.json()
        tracks.append(resp_json.get('items') or [])
        url = resp_json.get('next')
    tracks = sum(tracks, [])
    return tracks


async def get_audio_features(
    access_tokens: Text, track_ids: List[Text], limit: Optional[int] = 100
) -> List[Dict]:
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
    if not (0 < limit <= 100):
        limit = 100
        logger.warning(f'limit must be at most {limit}. setting value to {limit}')
    tracks = []
    size = len(track_ids)
    url = 'https://api.spotify.com/v1/audio-features?ids={}'
    for i in range(0, size, limit):
        current_tracks = ','.join(track_ids[i: i + limit])
        access_token = random.choice(access_tokens)
        response = await async_request(
            'get',
            url.format(current_tracks),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        resp_json = response.json()
        audio_features = resp_json.get('audio_features')
        if audio_features:
            tracks.append(audio_features)
    tracks = sum(tracks, [])
    return tracks


async def get_artists(
    access_tokens: Text, artist_ids: List[Text], limit: Optional[int] = 100
):
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
    if not (0 < limit <= 100):
        limit = 100
        logger.warning(f'limit must be at most {limit}. setting value to {limit}')
    artists = []
    size = len(artist_ids)
    url = 'https://api.spotify.com/v1/artists?ids={}'
    for i in range(0, size, limit):
        current_artists = ','.join(artist_ids[i: i + limit])
        access_token = random.choice(access_tokens)
        response = await async_request(
            'get',
            url.format(current_artists),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        resp_json = response.json()
        artists_info = resp_json.get('artists')
        if artists_info:
            artists.append(artists_info)
    artists = sum(artists, [])
    return artists
