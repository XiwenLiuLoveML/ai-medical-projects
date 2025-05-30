"""
chat_base.py

This module defines the core chat engine for the medical Q&A system,
including service initialization, LangGraph dialogue flow, and async streaming response.

Used in: LLM-Powered-Medical-Q&A-System (Demo Project)
"""

from contextlib import asynccontextmanager
from langgraph.graph import StateGraph, END, START
from typing import TypedDict, List, Optional, Union
from langchain_core.messages import HumanMessage, AIMessageChunk
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain_ollama import ChatOllama
from psycopg import AsyncConnection
from langgraph.graph import MessagesState
from backend.algorithms.llm.agent.rag_agent import gen_rag_graph
from config.settings import settings

DB_URI = (
    f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:'
    f'{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}'
)

OLLAMA_API_URL = settings.OLLAMA_API_URL
connection_kwargs = {'autocommit': True, 'prepare_threshold': 0}

class ChatService:
    """Singleton class that manages LLM chat flow and state persistence"""
    _instance: Optional['ChatService'] = None
    _app = None
    _checkpointer = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self):
        if self._app is None:
            conn = await AsyncConnection.connect(DB_URI, **connection_kwargs)
            self._checkpointer = AsyncPostgresSaver(conn)
            await self._checkpointer.setup()

            ollama_chat = ChatOllama(
                base_url=OLLAMA_API_URL,
                model='deepseek-r1:32b',
                temperature=0.8,
                num_predict=2560,
            )
            graph = gen_rag_graph(ollama_chat)
            self._app = graph.compile(checkpointer=self._checkpointer)

    @property
    def app(self):
        if self._app is None:
            raise RuntimeError('ChatService not initialized')
        return self._app

    @property
    def checkpointer(self):
        if self._checkpointer is None:
            raise RuntimeError('ChatService not initialized')
        return self._checkpointer

chat_service = ChatService()

def rewrite_query(query: dict) -> str:
    """Rewrite query to include context from search results or uploaded files"""
    if len(query.get('search_results', '')) > 0:
        search_results = '\n'.join([f['标题'] + f['搜索结果'] for f in query['search_results']])
        query['content'] = f'Answer based on the search results:\n{search_results}\n\nQuestion: {query["content"]}'
    if len(query.get('files', '')) > 0:
        file_result = '\n'.join([f['file_content'] for f in query['files']])
        query['content'] = f'Answer based on the file content:\n{file_result}\n\nQuestion: {query["content"]}'
    return query['content']

@asynccontextmanager
async def get_chat_service():
    """Async context for safely initializing chat service"""
    try:
        await chat_service.initialize()
        yield chat_service
    finally:
        pass

async def chat_generate(session_id: str, query: dict, kb_data: Union[dict, None]):
    """Async generator to stream LLM responses for a given session"""
    input_message = rewrite_query(query)
    async with get_chat_service() as service:
        config = {'configurable': {'thread_id': session_id}}
        state = {
            'messages': [input_message],
            'history': [],
            'kb_id': kb_data['kb_id'],
            'kb_name': kb_data['kb_name'],
            'kb_info': kb_data['kb_info'],
            'top_k': 5,
            'score_threshold': 0.7,
            'question': input_message,
            'docs': '',
            'retrieve_retry': 0,
        }

        try:
            async for msg in service.app.astream(state, stream_mode='messages', config=config):
                if msg[1]['langgraph_node'] == 'judge':
                    continue
                if not isinstance(msg[0], AIMessageChunk):
                    continue
                yield msg[0].content
        except Exception as e:
            yield f'Error: {str(e)}'
