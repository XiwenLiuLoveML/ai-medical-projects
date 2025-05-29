"""
This module defines the CRUD operations for user login logs,
used to monitor login behavior and security events in the system.
"""

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from app.medical.model import LoginLog
from app.medical.schema.login_log import CreateLoginLogParam


class CRUDLoginLog(CRUDPlus[LoginLog]):
    async def get_list(self, username: str | None = None, status: int | None = None, ip: str | None = None) -> Select:
        """
        Retrieve login log entries filtered by username, status, or IP address.
        """
        filters = {}
        if username is not None:
            filters.update(username__like=f'%{username}%')
        if status is not None:
            filters.update(status=status)
        if ip is not None:
            filters.update(ip__like=f'%{ip}%')
        return await self.select_order('created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj_in: CreateLoginLogParam) -> None:
        """
        Create a new login log entry.
        """
        await self.create_model(db, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        Delete login logs by ID.
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)

    async def delete_all(self, db: AsyncSession) -> int:
        """
        Delete all login log entries.
        """
        return await self.delete_model_by_column(db, allow_multiple=True)


# Data Access Object instance
login_log_dao: CRUDLoginLog = CRUDLoginLog(LoginLog)
