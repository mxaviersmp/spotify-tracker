import os
from datetime import datetime, timedelta
from typing import Dict, Mapping, Optional, Text

import requests
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from api.models import TokenData, UserModel
from sptf.spotify_db import User

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
OAUTH_AUTHORIZE_URL = os.getenv('OAUTH_AUTHORIZE_URL')
OAUTH_TOKEN_URL = os.getenv('OAUTH_TOKEN_URL')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = os.getenv('SCOPE')
B64_CLIENT = os.getenv('B64_CLIENT')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
TOKEN_DATA = {
    'client_id' : CLIENT_ID,
    'response_type' : 'code',
    'redirect_uri' : REDIRECT_URI,
    'scope': SCOPE
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def authorize_spotify():
    """
    Generates url for spotify authorization.

    Returns
    -------
    dict
        spotify authorization url
    """
    response = requests.get(OAUTH_AUTHORIZE_URL, params=TOKEN_DATA)
    url = response.url
    return {'spotify': url}


def create_access_token(
    data: Dict, expires_minutes: Optional[int] = ACCESS_TOKEN_EXPIRE_MINUTES
) -> Text:
    """
    Creates a jwt token from the data.

    Parameters
    ----------
    data : dict
        data to be encoded
    expires_delta : int, optional
        token expiration time, by default ACCESS_TOKEN_EXPIRE_MINUTES

    Returns
    -------
    str
        jwt token
    """
    to_encode = data.copy()
    if expires_minutes:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: Text) -> Mapping:
    """
    Decodes a jwt token.

    Parameters
    ----------
    token : str
        jwt token

    Returns
    -------
    mapping
        decoded token
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def authenticate_user(email: Text, password: Text) -> Optional[UserModel]:
    """
    Authenticates user  with email and password and return.

    Parameters
    ----------
    email : str
        user email
    password : str
        user password

    Returns
    -------
    UserMe
        user if valid
    """
    user = await User.objects.get(email=email)
    if user and verify_password(password, user.hashed_password):
        return UserModel(**user.dict())


def verify_password(plain_password: Text, hashed_password: Text) -> bool:
    """
    Verifies if password and password hash matches.

    Parameters
    ----------
    plain_password : str
        password
    hashed_password : str
        password hash

    Returns
    -------
    bool
        if passwords match
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: Text) -> Text:
    """
    Creates hash from password.

    Parameters
    ----------
    password : str
        password

    Returns
    -------
    str
        password hash
    """
    return pwd_context.hash(password)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserModel: # noqa
    """
    Gets user from token.

    Parameters
    ----------
    token : str, optional
        jwt token, by default Depends(oauth2_scheme)

    Returns
    -------
    UserMe
        user object

    Raises
    ------
    credentials_exception
        if jwt token is not valid
        if jwt token doesn't has userid
        if user doesn't exists
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode_access_token(token)
        userid = payload.get('sub')
        if userid is None:
            raise credentials_exception
        token_data = TokenData(id=userid)
    except JWTError:
        raise credentials_exception
    user = await User.objects.get(id=token_data.id)
    if user is None:
        raise credentials_exception
    user = UserModel(**user.dict())
    return user
