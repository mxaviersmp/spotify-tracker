
from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.security import (
    authenticate_user,
    authorize_spotify,
    create_access_token,
    get_password_hash,
)
from app.api.models import Token, UserModel, UserPassword, UserRefreshToken
from app.api.routers import users
from app.database.schema import User, UserToken, db
from app.etl.spotify_api import get_refresh_token, get_user_me

app = FastAPI(title='Spotify Stats', version='0.1.0')
app.include_router(users.router)


@app.on_event('startup')
async def startup():
    """Executes on application startup."""
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    """Executes on application shutdown."""
    await db.disconnect()


@app.get('/')
async def root():
    """Return status."""
    return {'status': 'ok'}


@app.get('/authorize', responses={307: {'description': 'Temporary Redirect'}})
async def authorize():
    """Redirects to spotify authorization."""
    url = authorize_spotify()
    return RedirectResponse(url.get('spotify'))


@app.post('/register', response_model=UserModel, status_code=201)
async def register(user: UserPassword = None):
    """Register user on the application."""
    user = user.dict()
    user['hashed_password'] = get_password_hash(user.pop('password'))
    user = await User.objects.create(**user)
    await UserToken.objects.create(user=user)
    return UserModel(**user.dict())


@app.get('/callback', response_model=UserRefreshToken)
async def callback(request: Request = None):
    """Callback from spotify authorization. Gets user refresh token and info."""
    code = request.query_params.get('code')
    tokens = get_refresh_token(code)

    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')
    user = get_user_me(access_token)
    user['refresh_token'] = refresh_token

    return UserRefreshToken(**user)


@app.post('/token', response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends()):  # noqa:B008
    """Authenticates user and creates an access token."""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(data={'sub': user.id})
    return {'access_token': access_token, 'token_type': 'bearer'}
