"""
Schema definitions for the login log module, used to record user login activities.
"""

from datetime import datetime
from pydantic import ConfigDict
from common.schema import SchemaBase


class LoginLogBase(SchemaBase):
    user_uuid: str
    username: str
    status: int
    ip: str
    country: str | None
    region: str | None
    city: str | None
    user_agent: str
    browser: str | None
    os: str | None
    device: str | None
    msg: str
    login_time: datetime


class CreateLoginLogParam(LoginLogBase):
    pass


class UpdateLoginLogParam(LoginLogBase):
    pass


class LoginLogDetail(LoginLogBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_time: datetime
