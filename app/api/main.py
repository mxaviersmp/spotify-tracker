from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from app import __version__
from app.api.crud.user import create_user
from app.api.dependencies.config import SETTINGS
from app.api.dependencies.security import (
    authenticate_user,
    authorize_spotify,
    create_access_token,
    get_password_hash,
)
from app.api.models import Token
from app.api.routers import items, user
from app.database.schema import db
from app.etl.spotify_api import get_refresh_token, get_user_me

app_version = __version__
app = FastAPI(
    title='Spotify Tracker',
    version=app_version,
    root_path=f'/{SETTINGS.app_env}'
)
app.include_router(user.router)
app.include_router(items.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=['x-apigateway-header', 'Content-Type', 'X-Amz-Date'],
)
app.state.database = db
templates = Jinja2Templates(directory=Path(__file__).resolve().parent / 'templates')


@app.on_event('startup')
async def startup():
    """Executes on application startup."""
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event('shutdown')
async def shutdown():
    """Executes on application shutdown."""
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


@app.get('/')
async def root():
    """Return status."""
    return {'status': 'ok', 'version': app_version}


@app.get(
    '/authorize',
    response_class=RedirectResponse,
    responses={status.HTTP_307_TEMPORARY_REDIRECT: {'description': 'Temporary Redirect'}}
)
async def authorize():
    """Redirects to spotify authorization."""
    url = authorize_spotify()
    return RedirectResponse(url.get('spotify'))


@app.get('/callback', response_class=HTMLResponse)
async def callback(request: Request = None):
    """Callback from spotify authorization. Gets user refresh token and info."""
    code = request.query_params.get('code')
    tokens = get_refresh_token(code)

    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')
    user = get_user_me(access_token)
    user['refresh_token'] = refresh_token

    return templates.TemplateResponse(
        'register.html',
        context={**user, 'request': request}
    )


@app.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
    id: str = Form(...),  # noqa:B008
    display_name: str = Form(...),  # noqa:B008
    email: str = Form(...),  # noqa:B008
    country: str = Form(...),  # noqa:B008
    uri: str = Form(...),  # noqa:B008
    href: str = Form(...),  # noqa:B008
    refresh_token: str = Form(...),  # noqa:B008
    password: str = Form(...)  # noqa:B008
):
    """Register user on the application."""
    user = {
        'id': id,
        'display_name': display_name,
        'email': email,
        'country': country,
        'uri': uri,
        'href': href,
        'refresh_token': refresh_token,
        'hashed_password': get_password_hash(password),
        'scopes': 'user'
    }
    user = await create_user(user)
    if not user:
        return JSONResponse(
            content='user already exists',
            status_code=status.HTTP_200_OK
        )
    return 'user created. please sign in'


@app.post('/token', response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends()):  # noqa:B008
    """Authenticates user and creates an access token."""
    user = await authenticate_user(
        form_data.username, form_data.password, form_data.scopes
    )
    access_token = create_access_token(data={'sub': user.id, 'scopes': form_data.scopes})
    return {'access_token': access_token, 'token_type': 'bearer'}
