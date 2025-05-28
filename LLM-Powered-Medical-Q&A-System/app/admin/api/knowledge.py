"""
knowledge.py — Public version for LLM-Powered Medical Q&A System

This module defines the knowledge base interface for uploading and managing medical documents.
It enables an LLM agent to retrieve domain knowledge from curated files.

Main Features:
- List available knowledge bases
- Upload, update, and delete medical documents
- Public-safe annotations only; internal business logic abstracted

This demo is part of the ongoing AI for Medicine showcase.
Full backend logic is implemented privately in `ai-private-core`
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Request, UploadFile, File, Path, Query
from pydantic import BaseModel

router = APIRouter()


# Dummy response schema for public API example
def success_response(data=None):
    return {"code": 200, "data": data or "success"}


class FileMetadata(BaseModel):
    file_id: int
    name: str
    tags: Optional[list[str]] = []


# List all medical knowledge base entries
@router.get("/kb/all", summary="List all medical knowledge bases")
async def list_knowledge_bases(request: Request):
    return success_response(data=[{"id": 1, "name": "Cardiology Protocols"}])


# Upload a document to a knowledge base
@router.post("/kb/{kb_id}/upload", summary="Upload document to medical knowledge base")
async def upload_document(
    kb_id: Annotated[int, Path(...)],
    file: UploadFile = File(...),
):
    # Demo only: in real system, this file will be embedded for LLM use
    return success_response()


# List files under a knowledge base
@router.get("/kb/{kb_id}/files", summary="List uploaded documents")
async def list_documents(
    kb_id: Annotated[int, Path(...)],
    search: Annotated[Optional[str], Query(description="Search file name or content")] = None,
):
    return success_response(data=[{"file_id": 101, "name": "Discharge Instructions.pdf"}])


# Modify file metadata
@router.put("/kb/file", summary="Update file metadata")
async def update_file_metadata(file_info: FileMetadata):
    return success_response()


# Delete a file from the knowledge base
@router.delete("/kb/file", summary="Delete document from KB")
async def delete_file(file_info: FileMetadata):
    return success_response()
