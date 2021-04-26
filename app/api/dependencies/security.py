from datetime import datetime, timedelta
from typing import Dict, List, Mapping, Optional, Text

import requests
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from app.api.crud.user import get_user
from app.api.dependencies.config import SETTINGS
from app.api.models import TokenData, UserModel

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='token',
    scopes={'user': 'Read information about the current user.', 'item': 'reads items'},
)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def authorize_spotify() -> Dict:
    """
    Generates url for spotify authorization.

    Returns
    -------
    dict
        spotify authorization url
    """
    response = requests.get(
        SETTINGS.oauth_authorize_url,
        params={
            'client_id' : SETTINGS.client_id,
            'response_type' : 'code',
            'redirect_uri' : SETTINGS.redirect_uri,
            'scope': SETTINGS.scope
        }
    )
    url = response.url
    return {'spotify': url}


def create_access_token(
    data: Dict,
    expires: Optional[bool] = True
) -> Text:
    """
    Creates a jwt token from the data.

    Parameters
    ----------
    data : dict
        data to be encoded
    expires: bool, optional
        wether the token expires, default True

    Returns
    -------
    str
        jwt token
    """
    to_encode = data.copy()
    if expires:
        expire = datetime.utcnow() + timedelta(
            minutes=SETTINGS.access_token_expire_minutes
        )
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SETTINGS.secret_key, algorithm=SETTINGS.algorithm)
    return encoded_jwt


def decode_access_token(
    token: Text
) -> Mapping:
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
    return jwt.decode(token, SETTINGS.secret_key, algorithms=[SETTINGS.algorithm])


async def authenticate_user(
    email: Text, password: Text, scopes: List[str]
) -> Optional[UserModel]:
    """
    Authenticates user  with email and password and return.

    Parameters
    ----------
    email : str
        user email
    password : str
        user password
    scopes : list of str
        user scopes

    Returns
    -------
    UserModel
        user if valid
    """
    authenticate_value = 'Bearer'
    user = await get_user({'email': email})
    if user and verify_password(password, user.hashed_password):
        user_scopes = user.scopes.split()
        for scope in scopes:
            if scope not in user_scopes:
                authenticate_value = f'Bearer scope="{" ".join(scopes)}"'
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Not enough permissions',
                    headers={'WWW-Authenticate': authenticate_value},
                )
        return UserModel(**user.dict())
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': authenticate_value},
    )


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


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)  # noqa:B008
) -> UserModel:
    """
    Gets user from token.

    Parameters
    ----------
    security_scopes: SecurityScopes
        scopes
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
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = 'Bearer'
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': authenticate_value},
    )
    try:
        payload = decode_access_token(token)
        userid = payload.get('sub')
        if userid is None:
            raise credentials_exception
        token_scopes = payload.get('scopes', [])
        token_data = TokenData(id=userid, scopes=token_scopes)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = await get_user({'id': token_data.id})
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not enough permissions',
                headers={'WWW-Authenticate': authenticate_value},
            )
    user = UserModel(**user.dict())
    return user
