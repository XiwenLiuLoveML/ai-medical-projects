"""
opera_log.py – REST API for tracking system operations (admin use)

Overview:
This module defines basic API endpoints for listing, deleting, and clearing user operation logs.
Useful for auditing actions such as create/edit/delete performed by admin users.

Note:
This is a simplified demo version, intended for LLM-powered systems that include an admin backend.
Remove this file if the Q&A system does not need internal audit logging.
"""

from typing import Annotated
from fastapi import APIRouter, Query

from app.admin.service.opera_log_service import opera_log_service
from common.response.response_schema import ResponseModel, response_base

router = APIRouter()

# GET: Fetch operation logs (optionally filtered)
@router.get("", summary="Fetch operation logs")
async def get_opera_logs(
    username: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
    ip: Annotated[str | None, Query()] = None,
) -> ResponseModel:
    logs = await opera_log_service.get_select(username=username, status=status, ip=ip)
    return response_base.success(data=[log.dict() for log in logs])

# DELETE: Delete selected operation logs
@router.delete("", summary="Delete selected operation logs")
async def delete_opera_logs(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await opera_log_service.delete(pk=pk)
    return response_base.success() if count > 0 else response_base.fail()

# DELETE: Clear all operation logs
@router.delete("/all", summary="Clear all operation logs")
async def clear_all_opera_logs() -> ResponseModel:
    count = await opera_log_service.delete_all()
    return response_base.success() if count > 0 else response_base.fail()
