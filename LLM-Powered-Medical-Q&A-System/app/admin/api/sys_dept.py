"""
sys_dept.py – Department (Medical Unit) Management API

Overview:
This module defines APIs to manage medical departments (e.g., Cardiology, Neurology),
allowing frontend admins to fetch, create, update, or remove department information.

Use case:
- Organizing Q&A entries by medical department
- Enabling department-based filtering or expert assignment
"""

from typing import Annotated
from fastapi import APIRouter, Path, Query

from app.admin.service.dept_service import dept_service
from app.admin.schema.dept import CreateDeptParam, UpdateDeptParam, GetDeptListDetails
from common.response.response_schema import ResponseModel, response_base
from utils.serializers import select_as_dict

router = APIRouter()

# Get department detail
@router.get("/{pk}", summary="Get department detail")
async def get_dept(pk: Annotated[int, Path(...)]) -> ResponseModel:
    dept = await dept_service.get(pk=pk)
    data = GetDeptListDetails(**select_as_dict(dept))
    return response_base.success(data=data)

# Get all departments as tree structure
@router.get("", summary="Get all departments as tree")
async def get_all_depts_tree(
    name: Annotated[str | None, Query()] = None,
    leader: Annotated[str | None, Query()] = None,
    phone: Annotated[str | None, Query()] = None,
    status: Annotated[int | str | None, Query()] = None,
) -> ResponseModel:
    status = None if status == "" else status
    dept = await dept_service.get_dept_tree(name=name, leader=leader, phone=phone, status=status)
    return response_base.success(data=dept)

# Create department
@router.post("", summary="Create department")
async def create_dept(obj: CreateDeptParam) -> ResponseModel:
    await dept_service.create(obj=obj)
    return response_base.success()

# Update department
@router.put("/{pk}", summary="Update department")
async def update_dept(pk: Annotated[int, Path(...)], obj: UpdateDeptParam) -> ResponseModel:
    count = await dept_service.update(pk=pk, obj=obj)
    return response_base.success() if count > 0 else response_base.fail()

# Delete department
@router.delete("/{pk}", summary="Delete department")
async def delete_dept(pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await dept_service.delete(pk=pk)
    return response_base.success() if count > 0 else response_base.fail()
