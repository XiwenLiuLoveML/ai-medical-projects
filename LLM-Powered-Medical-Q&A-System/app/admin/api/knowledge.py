"""
knowledge.py — Public version for LLM-Powered Medical Q&A System

This module defines the knowledge base interface for uploading and managing medical documents.
It enables an LLM agent to retrieve domain knowledge from curated files.

Main Features:
- List available knowledge bases
- Upload, update, and delete medical documents
- Public-safe annotations only; internal business logic abstracted

🔗 Related Components:
- knowledge_base_service: Handles CRUD logic for knowledge base
- chat_file_service: Handles file upload and file metadata operations
- schema.knowledge: Pydantic models for request/response

This demo is part of the ongoing AI for Medicine showcase.
Full backend logic is implemented privately in `ai-private-core`
"""


from typing import Annotated

from fastapi import APIRouter, Request, Path, UploadFile, File

from app.admin.service.knowledge_service import knowledge_base_service
from app.admin.service.llm_service import chat_file_service
from app.admin.schema.knowledge import (
    KnowledgeBaseCreateSchema,
    KnowledgeBaseUpdateSchema,
    KnowledgeBaseDeleteSchema,
    UpdateFileSchemaParam,
    KBFileSchema,
)

router = APIRouter()

# Create a new knowledge base
@router.post('/base/create')
async def create_knowledge_base(request: Request, obj: KnowledgeBaseCreateSchema):
    knowledge_base = await knowledge_base_service.create_base(obj=obj, user_id=request.user.id)
    return {"success": True, "data": knowledge_base}

# Update a knowledge base
@router.put('/base/update')
async def update_knowledge_base(request: Request, obj: KnowledgeBaseUpdateSchema):
    await knowledge_base_service.update_base(obj=obj, user_id=request.user.id)
    return {"success": True}

# Delete a knowledge base
@router.delete('/base/delete')
async def delete_knowledge_base(request: Request, obj: KnowledgeBaseDeleteSchema):
    await knowledge_base_service.delete_base(obj=obj, user_id=request.user.id)
    return {"success": True}

# Upload file to a knowledge base
@router.post('/base/{kb_id}/upload')
async def upload_file_to_kb(request: Request, kb_id: Annotated[int, Path(...)], file: UploadFile = File(...)):
    await chat_file_service.upload_knowledge_file(request.user.id, kb_id, file)
    return {"success": True}

# Update file info
@router.put('/base/file')
async def update_file_info(request: Request, obj: UpdateFileSchemaParam):
    await chat_file_service.update_file_info(request.user.id, obj=obj)
    return {"success": True}

# Delete a file from knowledge base
@router.delete('/base/file')
async def delete_file(request: Request, obj: KBFileSchema):
    await knowledge_base_service.delete_file(obj.kb_id, obj.file_id, request.user.id)
    return {"success": True}

