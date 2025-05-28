"""
login_log.py – REST API endpoints for login log management

Overview:
This file defines three simple API routes for managing user login logs in the system.
It includes:
- Fetching login logs (with optional filters)
- Deleting selected logs by primary key
- Clearing all logs

Use case:
These endpoints are useful for basic audit logging and admin-level oversight in an LLM-powered medical Q&A system.

Note:
This is a simplified version tailored for demonstration purposes, focusing on structure and clarity over full enterprise authentication and RBAC logic.
"""
from typing import Annotated
from fastapi import APIRouter, Query

from app.admin.service.login_log_service import login_log_service
from common.response.response_schema import ResponseModel, response_base

router = APIRouter()

# Endpoint to fetch login logs (optionally filter by username, status, or IP)
@router.get("", summary="Fetch login logs with optional filters")
async def get_login_logs(
    username: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
    ip: Annotated[str | None, Query()] = None,
) -> ResponseModel:
    logs = await login_log_service.get_select(username=username, status=status, ip=ip)
    return response_base.success(data=[log.dict() for log in logs])

# Endpoint to delete specific login logs by their primary keys
@router.delete("", summary="Delete selected login logs")
async def delete_login_logs(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await login_log_service.delete(pk=pk)
    return response_base.success() if count > 0 else response_base.fail()

# Endpoint to clear all login logs
@router.delete("/all", summary="Clear all login logs")
async def clear_all_login_logs() -> ResponseModel:
    count = await login_log_service.delete_all()
    return response_base.success() if count > 0 else response_base.fail()
