# token.py
# -----------------------------------------
# 📁 Description:
# Pydantic schemas for returning tokens after user login.
# Includes access token info and optional user details.
# -----------------------------------------

from datetime import datetime
from app.admin.schema.user import GetUserInfoNoRelationDetail
from common.schema import SchemaBase


class AccessTokenBase(SchemaBase):
    access_token: str
    access_token_type: str = 'Bearer'
    access_token_expire_time: datetime


class GetNewToken(AccessTokenBase):
    """Response for refreshing token"""
    pass


class GetLoginToken(AccessTokenBase):
    """Response after user login"""
    user: GetUserInfoNoRelationDetail
