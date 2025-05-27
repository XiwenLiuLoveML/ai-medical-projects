# app/router.py — Register modular API endpoints

from fastapi import APIRouter
from app.api.llm import router as llm_router

route = APIRouter(prefix="/api")

# 📣 Group routes under relevant tags for Swagger UI
route.include_router(llm_router, prefix="/llm", tags=["LLM Chat"])
