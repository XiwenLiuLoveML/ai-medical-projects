# This file defines the login log database operations for demonstration.
# It showcases a simplified CRUD structure for how login events are stored.
# Dependencies:
# - Model: app.model.login_log.LoginLog
# - Schema: app.schema.login_log.CreateLoginLogParam

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from app.model.login_log import LoginLog
from app.schema.login_log import CreateLoginLogParam


class CRUDLoginLog(CRUDPlus[LoginLog]):
    async def get_list(self, username: str | None = None) -> Select:
        """
        Retrieve login log records filtered by username (demo use only)
        """
        filters = {}
        if username is not None:
            filters.update(username__like=f"%{username}%")
        return await self.select_order("created_time", "desc", **filters)

    async def create(self, db: AsyncSession, obj_in: CreateLoginLogParam) -> None:
        """
        Create a new login log record
        """
        await self.create_model(db, obj_in, commit=True)


login_log_dao: CRUDLoginLog = CRUDLoginLog(LoginLog)
