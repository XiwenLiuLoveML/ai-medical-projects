# user.py (model version for Medical LLM Demo)
# -----------------------------------------
# 📁 Description:
# SQLAlchemy ORM model for User and SSOUser tables.
# Used for login authentication, token generation, and role/permission mapping.
# Simplified version for demo purposes.
# -----------------------------------------

from datetime import datetime
from typing import Union
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.model import Base, id_key
from database.db_mysql import uuid4_str
from utils.timezone import timezone


class User(Base):
    __tablename__ = 'sys_user'

    id: Mapped[id_key] = mapped_column(init=False)
    uuid: Mapped[str] = mapped_column(String(50), init=False, default_factory=uuid4_str, unique=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    nickname: Mapped[str] = mapped_column(String(20))
    password: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(50), index=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    status: Mapped[int] = mapped_column(default=1)
    is_multi_login: Mapped[bool] = mapped_column(default=False)
    avatar: Mapped[str | None] = mapped_column(String(255), default=None)
    join_time: Mapped[datetime] = mapped_column(init=False, default_factory=timezone.now)
    last_login_time: Mapped[datetime | None] = mapped_column(init=False)

    # Optional relations (simplified)
    dept_id: Mapped[int | None] = mapped_column(ForeignKey('sys_dept.id', ondelete='SET NULL'), default=None)


class SSOUser(Base):
    __tablename__ = 'sso_user'

    id: Mapped[id_key] = mapped_column(init=False)
    username: Mapped[str] = mapped_column(String(20), index=True)
    nickname: Mapped[str] = mapped_column(String(20))
    ticket: Mapped[str] = mapped_column(String(255))
    login_from: Mapped[str] = mapped_column(String(20))
