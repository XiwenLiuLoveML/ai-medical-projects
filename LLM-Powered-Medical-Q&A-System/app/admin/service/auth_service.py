# auth_service.py
# -----------------------------------------
# 📁 Description:
# This module implements the core login logic for the Medical LLM Q&A system.
# It handles user login via username/password and generates JWT tokens.
#
# 🔐 Related modules:
# - user_dao: Database access layer for user authentication
# - jwt: Token creation and validation logic
# - schema: Data models for login input and token output
# -----------------------------------------

from fastapi import Request, Response
from starlette.background import BackgroundTasks

from app.admin.crud.crud_user import user_dao
from app.admin.schema.token import GetLoginToken
from app.admin.schema.user import AuthLoginParam
from app.admin.service.login_log_service import login_log_service
from common.enums import LoginLogStatusType
from common.exception import errors
from common.security.jwt import (
    create_access_token,
    create_refresh_token,
    password_verify,
)
from database.db_mysql import async_db_session
from utils.timezone import timezone

class AuthService:
    @staticmethod
    async def login(*, request: Request, response: Response, obj: AuthLoginParam, background_tasks: BackgroundTasks) -> GetLoginToken:
        """Standard login with username and password, returns JWT tokens."""
        async with async_db_session.begin() as db:
            user = await user_dao.get_by_username(db, obj.username)
            if not user or not password_verify(obj.password, user.password):
                raise errors.AuthorizationError(msg='Invalid username or password')
            if not user.status:
                raise errors.AuthorizationError(msg='User is locked')
            access_token = await create_access_token(str(user.id), user.is_multi_login)
            refresh_token = await create_refresh_token(str(user.id), user.is_multi_login)
            background_tasks.add_task(
                login_log_service.create,
                db=db,
                request=request,
                user_uuid=user.uuid,
                username=user.username,
                login_time=timezone.now(),
                status=LoginLogStatusType.success.value,
                msg='Login successful',
            )
            await user_dao.update_login_time(db, user.username)
            await db.refresh(user)
            return GetLoginToken(
                access_token=access_token.access_token,
                access_token_expire_time=access_token.access_token_expire_time,
                user=user,
            )

auth_service = AuthService()
