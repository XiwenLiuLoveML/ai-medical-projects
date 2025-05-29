# user.py
# -----------------------------------------
# 📁 Description:
# Pydantic schema definitions for user authentication and user information.
# These models support login requests, user token payloads, and user info display.
#
# 🔗 Related modules:
# - dept.py / role.py: Optional references for expanded user info
# - StatusType: Enum for user status
# -----------------------------------------

from datetime import datetime
from pydantic import EmailStr, Field, HttpUrl, ConfigDict, model_validator
from typing_extensions import Self

from common.enums import StatusType
from common.schema import SchemaBase


# Basic login schema
class AuthSchemaBase(SchemaBase):
    username: str
    password: str | None


class AuthLoginParam(AuthSchemaBase):
    captcha: str


# Lightweight schema for adding a user
class AddUserParam(AuthSchemaBase):
    dept_id: int
    roles: list[int]
    nickname: str | None = None
    email: EmailStr | None = Field(default=None)
    is_staff: int | None = 1


# Basic user info (used for token and current user display)
class GetUserInfoNoRelationDetail(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: str
    username: str
    nickname: str
    email: EmailStr | None = None
    avatar: str | None = None
    status: StatusType = Field(default=StatusType.enable)
    is_superuser: bool
    is_staff: bool
    is_multi_login: bool
    join_time: datetime = None
    last_login_time: datetime | None = None


class GetCurrentUserInfoDetail(GetUserInfoNoRelationDetail):
    model_config = ConfigDict(from_attributes=True)

    dept: str | None = None
    roles: list[str] | None = None

    @model_validator(mode='after')
    def convert_objects_to_names(self) -> Self:
        """Convert role/dept objects to their names for frontend display."""
        if self.dept and hasattr(self.dept, 'name'):
            self.dept = self.dept.name  # type: ignore
        if self.roles and isinstance(self.roles[0], dict):
            self.roles = [r['name'] for r in self.roles]  # type: ignore
        return self
