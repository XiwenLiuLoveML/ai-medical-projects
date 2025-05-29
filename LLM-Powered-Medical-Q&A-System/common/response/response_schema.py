# response_schema.py
# -----------------------------------------
# 📁 Description:
# Provides unified response format for all API endpoints.
# Standard structure:
# {
#   "code": 200,
#   "msg": "Success",
#   "data": {...}
# }
#
# Supports:
# - success(): normal response with validation
# - fail(): failure response
# - fast_success(): fast JSON response (skip pydantic validation)
# -----------------------------------------

from datetime import datetime
from typing import Any

from fastapi import Response
from pydantic import BaseModel, ConfigDict
from starlette.responses import JSONResponse

from common.response.response_code import CustomResponse, CustomResponseCode
from config.settings import settings


class ResponseModel(BaseModel):
    """Standard API response"""
    model_config = ConfigDict(json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)})

    code: int = CustomResponseCode.HTTP_200.code
    msg: str = CustomResponseCode.HTTP_200.msg
    data: Any | None = None


class ResponseBase:
    def success(self, *, res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_200, data: Any = None) -> ResponseModel:
        return ResponseModel(code=res.code, msg=res.msg, data=data)

    def fail(self, *, res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_400, data: Any = None) -> ResponseModel:
        return ResponseModel(code=res.code, msg=res.msg, data=data)

    def fast_success(self, *, res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_200, data: Any | None = None) -> Response:
        return JSONResponse({'code': res.code, 'msg': res.msg, 'data': data})


response_base = ResponseBase()
custom_encoder = {datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S')}
