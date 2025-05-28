"""
sys_dict_data.py – Medical Field Value Dictionary API

Overview:
Provides basic endpoints for managing predefined value sets (dictionaries),
such as gender, disease stage, education level, or appointment types.

Use case:
- Populate dropdowns for patient intake forms
- Use structured values in LLM-based prompts
- Support multilingual display of option labels
"""

from typing import Annotated
from fastapi import APIRouter, Path, Query

from app.admin.service.dict_data_service import dict_data_service
from app.admin.schema.dict_data import CreateDictDataParam, UpdateDictDataParam, GetDictDataListDetails
from common.response.response_schema import ResponseModel, response_base
from utils.serializers import select_as_dict

router = APIRouter()

# Get dictionary entry by ID
@router.get("/{pk}", summary="Get dictionary entry detail")
async def get_dict_data(pk: Annotated[int, Path(...)]) -> ResponseModel:
    dict_data = await dict_data_service.get(pk=pk)
    data = GetDictDataListDetails(**select_as_dict(dict_data))
    return response_base.success(data=data)

# List all dictionary entries (with filters)
@router.get("", summary="List dictionary entries")
async def get_dict_entries(
    label: Annotated[str | None, Query()] = None,
    value: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
) -> ResponseModel:
    entries = await dict_data_service.get_select(label=label, value=value, status=status)
    return response_base.success(data=[e.dict() for e in entries])

# Create dictionary entry
@router.post("", summary="Create dictionary entry")
async def create_dict_data(obj: CreateDictDataParam) -> ResponseModel:
    await dict_data_service.create(obj=obj)
    return response_base.success()

# Update dictionary entry
@router.put("/{pk}", summary="Update dictionary entry")
async def update_dict_data(pk: Annotated[int, Path(...)], obj: UpdateDictDataParam) -> ResponseModel:
    count = await dict_data_service.update(pk=pk, obj=obj)
    return response_base.success() if count > 0 else response_base.fail()

# Delete entries
@router.delete("", summary="Delete dictionary entries")
async def delete_dict_data(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await dict_data_service.delete(pk=pk)
    return response_base.success() if count > 0 else response_base.fail()
