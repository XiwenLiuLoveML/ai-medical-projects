# jwt.py
# -----------------------------------------
# 📁 Description:
# This module handles JWT-based authentication including:
# - Token generation (access & refresh)
# - Token decoding
# - Password hashing and verification
# - User fetching via token
# -----------------------------------------

from datetime import timedelta
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from jose import ExpiredSignatureError, JWTError, jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.model import User
from app.admin.schema.user import CurrentUserIns
from common.dataclasses import AccessToken, NewToken, RefreshToken
from common.exception.errors import AuthorizationError, TokenError
from config.settings import settings
from database.db_mysql import async_db_session
from utils.serializers import select_as_dict
from utils.timezone import timezone

password_hash = PasswordHash((BcryptHasher(),))


def get_hash_password(password: str, salt: bytes | None) -> str:
    return password_hash.hash(password, salt=salt)


def password_verify(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


async def create_access_token(sub: str, multi_login: bool) -> AccessToken:
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
    to_encode = {'exp': expire, 'sub': sub}
    access_token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    return AccessToken(access_token=access_token, access_token_expire_time=expire)


async def create_refresh_token(sub: str, multi_login: bool) -> RefreshToken:
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    to_encode = {'exp': expire, 'sub': sub}
    refresh_token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    return RefreshToken(refresh_token=refresh_token, refresh_token_expire_time=expire)


def get_token(request: Request) -> str:
    authorization = request.headers.get('Authorization')
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != 'bearer':
        raise TokenError(msg='Invalid Token')
    return token


def jwt_decode(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        user_id = int(payload.get('sub'))
        if not user_id:
            raise TokenError(msg='Invalid Token')
    except ExpiredSignatureError:
        raise TokenError(msg='Token expired')
    except (JWTError, Exception):
        raise TokenError(msg='Invalid Token')
    return user_id


async def get_current_user(db: AsyncSession, pk: int) -> User:
    from app.admin.crud.crud_user import user_dao
    user = await user_dao.get_with_relation(db, user_id=pk)
    if not user or not user.status:
        raise AuthorizationError(msg='Invalid or inactive user')
    return user


async def jwt_authentication(token: str) -> CurrentUserIns:
    user_id = jwt_decode(token)
    async with async_db_session() as db:
        current_user = await get_current_user(db, user_id)
        return CurrentUserIns(**select_as_dict(current_user))
