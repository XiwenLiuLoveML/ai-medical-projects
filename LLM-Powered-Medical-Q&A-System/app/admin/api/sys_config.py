"""
sys_config.py – Public-facing configuration API (Simplified for Medical Q&A System)

Overview:
Provides endpoints to fetch and update protocol, policy, and website metadata.
Useful for compliance and informational display on the user-facing platform.

Note:
This is a simplified version, focusing only on agreement-related configs.
"""

from typing import Annotated
from fastapi import APIRouter
from app.admin.service.config_service import config_service
from app.admin.schema.config import SaveConfigParam
from common.response.response_schema import ResponseModel, response_base

router = APIRouter()

# User agreement
@router.get("/protocol", summary="Get user agreement")
async def get_protocol_config() -> ResponseModel:
    config = await config_service.get_built_in_config("protocol")
    return response_base.success(data=config)

@router.post("/protocol", summary="Update user agreement")
async def save_protocol_config(objs: list[SaveConfigParam]) -> ResponseModel:
    await config_service.save_built_in_config(objs, "protocol")
    return response_base.success()

# Privacy policy
@router.get("/policy", summary="Get privacy policy")
async def get_policy_config() -> ResponseModel:
    config = await config_service.get_built_in_config("policy")
    return response_base.success(data=config)

@router.post("/policy", summary="Update privacy policy")
async def save_policy_config(objs: list[SaveConfigParam]) -> ResponseModel:
    await config_service.save_built_in_config(objs, "policy")
    return response_base.success()
