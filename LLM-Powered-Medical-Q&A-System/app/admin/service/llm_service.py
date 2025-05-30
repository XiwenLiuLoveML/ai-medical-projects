# Filename: llm_service.py
# Description:
#   This file contains the service layer for managing core logic in the LLM-powered medical Q&A system.
#   Includes session handling, message saving, and file uploads.
#   This version is simplified for open-source demonstration and omits proprietary logic such as Celery tasks,
#   vector indexing, and internal data relationships.

import os
import uuid
from typing import Any, List, Optional

from fastapi import UploadFile

from app.schema.llm import (
    LLmChat,
    ChatSessionBase,
    CreateChatMessageParam,
    CreateChatFileParam,
    GetChatFileDetail,
)
from app.model import Chat, ChatSession, ChatMessage, ChatFile
from app.crud import chat_dao, chat_session_dao, chat_message_dao, chat_file_dao

from utils.file_ops import upload_file, build_filename
from config.path_conf import LLM_CHAT_DIR
from algorithms.llm.document_loaders import file_parse
from database.db_mysql import async_db_session
from common.exception import errors


class ChatSessionService:
    """Handles creation, update, and retrieval of chat sessions."""

    @staticmethod
    async def get_by_session_id(session_id: str) -> ChatSession:
        async with async_db_session() as db:
            session = await chat_session_dao.get_by_session_id(db, session_id)
            if not session:
                raise errors.NotFoundError(msg='Session not found')
            return session

    @staticmethod
    async def create(obj: ChatSession) -> None:
        async with async_db_session.begin() as db:
            await chat_session_dao.create(db, obj)

    @staticmethod
    async def update(obj: ChatSessionBase) -> int:
        async with async_db_session.begin() as db:
            session = await chat_session_dao.get_by_session_id(db, obj.session_id)
            if not session:
                raise errors.NotFoundError(msg='Session not found')
            return await chat_session_dao.update(db, session.id, obj)

    @staticmethod
    async def delete_by_session_id(session_id: str) -> int:
        async with async_db_session.begin() as db:
            return await chat_session_dao.soft_delete(db, session_id)


class ChatMessageService:
    """Handles creation and retrieval of chat messages."""

    @staticmethod
    async def create(obj: CreateChatMessageParam) -> int:
        async with async_db_session.begin() as db:
            return await chat_message_dao.create(db, obj)

    @staticmethod
    async def get_by_session_id(session_id: str) -> List[ChatMessage]:
        async with async_db_session() as db:
            messages = await chat_message_dao.get_by_session_id(db, session_id)
            # Optional: attach file info if needed
            for message in messages:
                if message.files:
                    file_ids = message.files.split(',')
                    files = await chat_file_service.get_by_ids(file_ids=file_ids)
                    message.files = [GetChatFileDetail(**vars(f)) for f in files]
            return messages


class ChatFileService:
    """Handles uploading and reading chat-related documents."""

    @staticmethod
    async def upload_file(user_id: int, file: UploadFile) -> dict:
        if not os.path.exists(LLM_CHAT_DIR):
            os.makedirs(LLM_CHAT_DIR)

        filename = build_filename(file)
        file_path = os.path.join(LLM_CHAT_DIR, filename)
        await upload_file(file, file_path)

        file_id = str(uuid.uuid4())
        file_size = os.path.getsize(file_path)
        file_content = file_parse(file_path)

        file_obj = CreateChatFileParam(
            user_id=user_id,
            status='SUCCESS',
            file_id=file_id,
            file_name=file.filename,
            file_size=file_size,
            file_path=filename,
            file_content=file_content,
        )

        async with async_db_session.begin() as db:
            await chat_file_dao.create(db, file_obj)

        return {
            'file_id': file_id,
            'file_name': file.filename,
            'file_size': file_size,
        }

    @staticmethod
    async def get_by_ids(file_ids: List[str]) -> List[ChatFile]:
        async with async_db_session() as db:
            return await chat_file_dao.get_by_ids(db, file_ids)


# Service instances for API access
chat_session_service = ChatSessionService()
chat_message_service = ChatMessageService()
chat_file_service = ChatFileService()
