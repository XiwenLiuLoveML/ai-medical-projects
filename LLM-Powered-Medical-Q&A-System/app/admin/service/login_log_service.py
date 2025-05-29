#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🩺 Login Log Service (Public Demo Version)
This is a simplified version for public-facing projects.
It records only basic login activity without storing sensitive device or regional data.
"""

from datetime import datetime

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.crud.crud_login_log import login_log_dao
from app.admin.schema.login_log import CreateLoginLogParam


class LoginLogService:
    @staticmethod
    async def create(
        *,
        db: AsyncSession,
        request: Request,
        user_uuid: str,
        username: str,
        login_time: datetime,
        status: int,
        msg: str,
    ) -> None:
        obj_in = CreateLoginLogParam(
            user_uuid=user_uuid,
            username=username,
            status=status,
            ip=request.client.host,  # Minimal: only store IP
            msg=msg,
            login_time=login_time,
        )
        await login_log_dao.create(db, obj_in)


login_log_service: LoginLogService = LoginLogService()
