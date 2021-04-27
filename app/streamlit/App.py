import altair as alt
import pandas as pd
import requests
import streamlit as st
from SessionState import get

session_state = get(token='')


def get_played_tracks(token):
    response = requests.get(
        'http://localhost:8000/user/played-tracks',
        headers={
            'Content-Type': 'accept: application/json',
            'Authorization': f'Bearer {token}'
        }
    )
    played_tracks = response.json()
    played_tracks = pd.DataFrame(played_tracks)
    played_tracks['track'] = played_tracks['track'].apply(
        lambda x: x.get('name')
    )
    return played_tracks


def get_tracks(token):
    response = requests.get(
        'http://localhost:8000/user/tracks',
        headers={
            'Content-Type': 'accept: application/json',
            'Authorization': f'Bearer {token}'
        }
    )
    tracks = response.json()
    tracks = pd.DataFrame(tracks)
    return tracks.sort_values(by='count')


def get_artists(token):
    response = requests.get(
        'http://localhost:8000/user/artists',
        headers={
            'Content-Type': 'accept: application/json',
            'Authorization': f'Bearer {token}'
        }
    )
    artists = response.json()
    artists = pd.DataFrame(artists)
    return artists.sort_values(by='count')


def get_audio_features(token):
    response = requests.get(
        'http://localhost:8000/user/audio-features',
        headers={
            'Content-Type': 'accept: application/json',
            'Authorization': f'Bearer {token}'
        }
    )
    audio_features = response.json()
    audio_features = pd.DataFrame(audio_features)
    return [alt.Chart(audio_features).mark_bar().encode(
        alt.X(feature, bin=True),
        y='count()',
    ) for feature in audio_features.columns]


def get_genres(token):
    response = requests.get(
        'http://localhost:8000/user/genres',
        headers={
            'Content-Type': 'accept: application/json',
            'Authorization': f'Bearer {token}'
        }
    )
    genres = response.json()
    genres = pd.DataFrame({'x': genres.keys(), 'y': genres.values()})
    return alt.Chart(genres).mark_bar().encode(
        x='x',
        y='y'
    )


def main():
    st.header('Spotify Tracker')
    if st.button('played-tracks'):
        played_tracks = get_played_tracks(session_state.token)
        st.write(played_tracks)
    if st.button('tracks'):
        tracks = get_tracks(session_state.token)
        st.write(tracks)
    if st.button('artists'):
        artists = get_artists(session_state.token)
        st.write(artists)
    if st.button('audio-features'):
        audio_features = get_audio_features(session_state.token)
        _ = [st.write(feat) for feat in audio_features]
    if st.button('genres'):
        genres = get_genres(session_state.token)
        st.write(genres)


if not session_state.token:
    usr_placeholder = st.sidebar.empty()
    pwd_placeholder = st.sidebar.empty()
    usr = usr_placeholder.text_input('Email:', value='', type='default')
    pwd = pwd_placeholder.text_input('Password:', value='', type='password')
    if usr and pwd:
        payload = {
            'username': usr,
            'password': pwd,
            'scope': 'user'
        }
        response = requests.post(
            'http://localhost:8000/token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=payload
        )
        session_state.token = response.json().get('access_token')
    if session_state.token:
        pwd_placeholder.empty()
        usr_placeholder.empty()
        usr = None
        pwd = None
        main()
    else:
        st.error('the password you entered is incorrect')
else:
    if st.button('logout'):
        session_state.token = None
    main()
