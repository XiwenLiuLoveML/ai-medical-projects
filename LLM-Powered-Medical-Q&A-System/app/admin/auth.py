"""
auth.py — Minimal demo authentication API

This module showcases a simplified authentication API powered by FastAPI, designed for medical Q&A systems.
It includes basic endpoints for user login, logout, info retrieval, and token refresh.

🔒 Core authentication logic is abstracted in the private repository `ai-private-core`.
This is a public-facing demo to illustrate API structure only.
"""

from fastapi import APIRouter, Depends, Request, Response
from starlette.background import BackgroundTasks

from app.admin.schema.user import AuthSchemaBase  # 🔹 Data schema for login input
from app.admin.service.auth_service import auth_service  # 🔹 Service layer for handling login logic
from common.response.response_schema import ResponseModel, response_base  # 🔹 Standard API response format
from common.security.jwt import DependsJwtAuth  # 🔹 JWT-based token authentication dependency

# 🔹 Create a FastAPI router for authentication-related routes
med_auth_router = APIRouter()

@med_auth_router.post("/user/login", summary="User Login")
async def user_login(
    request: Request,
    response: Response,
    obj: AuthSchemaBase,
    background_tasks: BackgroundTasks,
) -> ResponseModel:
    """
    Accepts login credentials (username + password) and returns an access token.
    Typically used by frontend/mobile clients for session management.
    """
    data = await auth_service.login(request=request, response=response, obj=obj, background_tasks=background_tasks)
    return response_base.success(data=data)


@med_auth_router.get("/user/info", summary="Get User Info")
async def get_user_info(request: Request):
    """
    Retrieves basic user profile from request context.
    Requires prior JWT authentication.
    This endpoint is useful for displaying user dashboards.
    """
    dummy_avatar = "https://example.com/avatar.png"
    data = {
        "roles": [role.name for role in request.user.roles],  # 🔹 User roles, e.g., admin/doctor
        "name": request.user.nickname,  # 🔹 User display name
        "avatar": request.user.avatar or dummy_avatar,  # 🔹 Fallback avatar if none present
    }
    return response_base.fast_success(data=data)


@med_auth_router.post("/user/logout", summary="User Logout")
async def user_logout(request: Request):
    """
    Dummy logout endpoint for stateless authentication.
    In a real app, this might include token blacklisting logic.
    """
    return {"code": 200, "data": "success"}


@med_auth_router.post("/token/new", summary="Refresh Token", dependencies=[DependsJwtAuth])
async def create_new_token(request: Request, response: Response) -> ResponseModel:
    """
    Refresh JWT token before it expires.
    Allows clients to maintain continuous authentication.
    Requires valid JWT.
    """
    data = await auth_service.new_token(request=request, response=response)
    return response_base.success(data=data)
