"""
sys_dict_type.py – Dictionary Type Management API

Overview:
Defines APIs to manage categories of dictionary values,
such as gender, education_level, or appointment_type.

Use case:
- Enables flexible configuration of field value types
- Supports LLM prompt generation or frontend form options
"""

from typing import Annotated
from fastapi import APIRouter, Path, Query

from app.admin.service.dict_type_service import dict_type_service
from app.admin.schema.dict_type import CreateDictTypeParam, UpdateDictTypeParam, GetDictTypeListDetails
from common.response.response_schema import ResponseModel, response_base

router = APIRouter()

# List all dictionary types
@router.get("", summary="List all dictionary types")
async def get_dict_types(
    name: Annotated[str | None, Query()] = None,
    code: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
) -> ResponseModel:
    result = await dict_type_service.get_select(name=name, code=code, status=status)
    return response_base.success(data=[r.dict() for r in result])

# Create a new dictionary type
@router.post("", summary="Create dictionary type")
async def create_dict_type(obj: CreateDictTypeParam) -> ResponseModel:
    await dict_type_service.create(obj=obj)
    return response_base.success()

# Update dictionary type
@router.put("/{pk}", summary="Update dictionary type")
async def update_dict_type(pk: Annotated[int, Path(...)], obj: UpdateDictTypeParam) -> ResponseModel:
    count = await dict_type_service.update(pk=pk, obj=obj)
    return response_base.success() if count > 0 else response_base.fail()

# Delete dictionary types
@router.delete("", summary="Delete dictionary types")
async def delete_dict_type(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await dict_type_service.delete(pk=pk)
    return response_base.success() if count > 0 else response_base.fail()
