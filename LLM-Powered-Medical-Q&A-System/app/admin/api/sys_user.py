"""
sys_user.py – User Management API

Overview:
Manages registration, profile updates, role assignments, and deletion.
Simplified for LLM-based medical platform with doctors, patients, and admin users.

Use case:
- Patient self-registration
- Doctor profile updates
- Admin-controlled role permissions
"""

from typing import Annotated
from fastapi import APIRouter, Path, Query, Request

from app.admin.service.user_service import user_service
from app.admin.schema.user import (
    RegisterUserParam, AddUserParam, UpdateUserAllParam,
    GetCurrentUserInfoDetail, GetUserInfoListDetails
)
from common.response.response_schema import ResponseModel, response_base
from utils.serializers import select_as_dict

user_router = APIRouter()

@user_router.post("/register", summary="Register new user")
async def register_user(obj: RegisterUserParam) -> ResponseModel:
    await user_service.register(obj=obj)
    return response_base.success()

@user_router.post("/add", summary="Admin add user")
async def add_user(request: Request, obj: AddUserParam) -> ResponseModel:
    await user_service.add(request=request, obj=obj)
    user = await user_service.get_userinfo(username=obj.username)
    data = GetUserInfoListDetails(**select_as_dict(user))
    return response_base.success(data=data)

@user_router.get("/me", summary="Get current user info")
async def get_current_user(request: Request) -> ResponseModel:
    data = GetCurrentUserInfoDetail(**request.user.model_dump())
    return response_base.success(data=data)

@user_router.get("/{username}", summary="Get user info")
async def get_user(username: Annotated[str, Path(...)]) -> ResponseModel:
    user = await user_service.get_userinfo(username=username)
    data = GetUserInfoListDetails(**select_as_dict(user))
    return response_base.success(data=data)

@user_router.put("/{username}", summary="Update user info")
async def update_user(request: Request, username: Annotated[str, Path(...)], obj: UpdateUserAllParam) -> ResponseModel:
    count = await user_service.update(request=request, username=username, obj=obj)
    return response_base.success() if count > 0 else response_base.fail()

@user_router.delete("/{username}", summary="Delete user")
async def delete_user(username: Annotated[str, Path(...)]) -> ResponseModel:
    count = await user_service.delete(username=username)
    return response_base.success() if count > 0 else response_base.fail()
