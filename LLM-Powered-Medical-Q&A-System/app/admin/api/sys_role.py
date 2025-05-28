"""
sys_role.py – Role Management API

Overview:
Provides APIs for managing user roles such as 'Doctor', 'Nurse', or 'Admin'.
Each role may control access to different features or UI components.

Use case:
- Assign permissions to different user types
- Configure sidebar/menu visibility
"""

from typing import Annotated
from fastapi import APIRouter, Path, Query, Request

from app.admin.service.role_service import role_service
from app.admin.service.menu_service import menu_service
from app.admin.schema.role import CreateRoleParam, UpdateRoleParam, UpdateRoleMenuParam, GetRoleListDetails
from common.response.response_schema import ResponseModel, response_base
from utils.serializers import select_as_dict, select_list_serialize

router = APIRouter()

# Get all roles
@router.get("/all", summary="List all roles")
async def get_all_roles() -> ResponseModel:
    roles = await role_service.get_all()
    data = select_list_serialize(roles)
    return response_base.success(data=data)

# Get roles for a specific user
@router.get("/{pk}/all", summary="Get roles for a user")
async def get_user_all_roles(pk: Annotated[int, Path(...)]) -> ResponseModel:
    roles = await role_service.get_user_roles(pk=pk)
    data = select_list_serialize(roles)
    return response_base.success(data=data)

# Get menu tree for a role
@router.get("/{pk}/menus", summary="Get role's menus")
async def get_role_all_menus(pk: Annotated[int, Path(...)]) -> ResponseModel:
    menu = await menu_service.get_role_menu_tree(pk=pk)
    return response_base.success(data=menu)

# Get role detail
@router.get("/{pk}", summary="Get role detail")
async def get_role(pk: Annotated[int, Path(...)]) -> ResponseModel:
    role = await role_service.get(pk=pk)
    data = GetRoleListDetails(**select_as_dict(role))
    return response_base.success(data=data)

# Create role
@router.post("", summary="Create role")
async def create_role(obj: CreateRoleParam) -> ResponseModel:
    await role_service.create(obj=obj)
    return response_base.success()

# Update role
@router.put("/{pk}", summary="Update role")
async def update_role(pk: Annotated[int, Path(...)], obj: UpdateRoleParam) -> ResponseModel:
    count = await role_service.update(pk=pk, obj=obj)
    return response_base.success() if count > 0 else response_base.fail()

# Update role-menu bindings
@router.put("/{pk}/menu", summary="Update role menus")
async def update_role_menus(request: Request, pk: int, menu_ids: UpdateRoleMenuParam) -> ResponseModel:
    count = await role_service.update_role_menu(request=request, pk=pk, menu_ids=menu_ids)
    return response_base.success() if count > 0 else response_base.fail()

# Delete roles
@router.delete("", summary="Delete roles")
async def delete_role(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await role_service.delete(pk=pk)
    return response_base.success() if count > 0 else response_base.fail()
