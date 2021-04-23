from typing import List

from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from api.models import PlayedTrackModel, Token, UserModel, UserPassword, UserRefreshToken
from api.security import (
    authenticate_user,
    authorize_spotify,
    create_access_token,
    get_current_user,
    get_password_hash,
)
from sptf.spotify_api import get_refresh_token, get_user_me
from sptf.spotify_db import PlayedTrack, User, UserToken, db

app = FastAPI()


@app.on_event('startup')
async def startup():
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect()


@app.get('/')
async def root():
    return {'status': 'ok'}


@app.get('/authorize', responses={307: {'description': 'Temporary Redirect'}})
async def authorize():
    url = authorize_spotify()
    return RedirectResponse(url.get('spotify'))


@app.post('/register', response_model=UserModel, status_code=201)
async def register(user: UserPassword = None):
    user = user.dict()
    user['hashed_password'] = get_password_hash(user.pop('password'))
    user = await User.objects.create(**user)
    await UserToken.objects.create(user=user)
    return UserModel(**user.dict())


@app.get('/callback', response_model=UserRefreshToken)
async def callback(request: Request = None):
    code = request.query_params.get('code')
    tokens = get_refresh_token(code)

    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')
    user = get_user_me(access_token)
    user['refresh_token'] = refresh_token

    return UserRefreshToken(**user)


@app.post('/token', response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends()): # noqa
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(data={'sub': user.id})
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/users/me', response_model=UserModel, tags=['users'])
async def me(current_user: UserModel = Depends(get_current_user)): # noqa
    return current_user


@app.get('/users/me/played-tracks', response_model=List[PlayedTrackModel], tags=['users'])
async def played_tracks(current_user: UserModel = Depends(get_current_user)): # noqa
    played_tracks = await PlayedTrack.objects.select_related(
        ['artist', 'track']
    ).all(user=current_user.id)
    return played_tracks
