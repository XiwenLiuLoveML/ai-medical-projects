"""
sys_menu.py – Menu Management API

Overview:
Provides APIs to manage menu items in a backend admin panel.
Enables tree structure routing and dynamic sidebar based on user role.

Use case:
- Used in doctor/administrator backend dashboard
- Structure menus like “Departments”, “Knowledge Base”, “Protocol Settings”
"""

from typing import Annotated
from fastapi import APIRouter, Path, Query, Request

from app.admin.service.menu_service import menu_service
from app.admin.schema.menu import CreateMenuParam, UpdateMenuParam, GetMenuListDetails
from common.response.response_schema import ResponseModel, response_base
from utils.serializers import select_as_dict

router = APIRouter()

# Get current user's sidebar menu
@router.get("/sidebar", summary="Get current user's sidebar menu")
async def get_user_sidebar_tree(request: Request) -> ResponseModel:
    menu = await menu_service.get_user_menu_tree(request=request)
    return response_base.success(data=menu)

# Get single menu detail
@router.get("/{pk}", summary="Get menu detail")
async def get_menu(pk: Annotated[int, Path(...)]) -> ResponseModel:
    menu = await menu_service.get(pk=pk)
    data = GetMenuListDetails(**select_as_dict(menu))
    return response_base.success(data=data)

# List all menus (tree structure)
@router.get("", summary="List all menus")
async def get_all_menus(
    title: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
) -> ResponseModel:
    menu = await menu_service.get_menu_tree(title=title, status=status)
    return response_base.success(data=menu)

# Create a new menu item
@router.post("", summary="Create new menu")
async def create_menu(obj: CreateMenuParam) -> ResponseModel:
    await menu_service.create(obj=obj)
    return response_base.success()

# Update a menu item
@router.put("/{pk}", summary="Update menu")
async def update_menu(pk: Annotated[int, Path(...)], obj: UpdateMenuParam) -> ResponseModel:
    count = await menu_service.update(pk=pk, obj=obj)
    return response_base.success() if count > 0 else response_base.fail()

# Delete a menu item
@router.delete("/{pk}", summary="Delete menu")
async def delete_menu(pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await menu_service.delete(pk=pk)
    return response_base.success() if count > 0 else response_base.fail()
