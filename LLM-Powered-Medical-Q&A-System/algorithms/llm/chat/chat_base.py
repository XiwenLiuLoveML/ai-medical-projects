"""
📍 Path: backend/algorithms/llm/chat

📌 This module implements the base conversational interface powered by LLMs,
supporting knowledge base Q&A with optional retrieval.

Key Features:
- LangGraph-based dialogue flow
- Ollama-backed LLM (e.g., DeepSeek-R1)
- Async streaming reply generation
"""

from langgraph.graph import StateGraph, START, END
from typing import Union
from langchain_core.messages import AIMessageChunk
from langchain_ollama import ChatOllama
from contextlib import asynccontextmanager

from algorithms.llm.agent.rag_agent import gen_rag_graph  # defines the LangGraph pipeline
from config.settings import settings  # environment config loader

# Set up model endpoint (from environment)
OLLAMA_API_URL = settings.OLLAMA_API_URL


# Singleton ChatService
class ChatService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._app = None
        return cls._instance

    async def initialize(self):
        if self._app is None:
            ollama_chat = ChatOllama(
                base_url=OLLAMA_API_URL,
                model='deepseek-r1:32b',
                temperature=0.8,
                num_predict=2560,
            )
            graph = gen_rag_graph(ollama_chat)
            self._app = graph.compile()

    @property
    def app(self):
        if self._app is None:
            raise RuntimeError("ChatService not initialized")
        return self._app


# Global instance
chat_service = ChatService()


@asynccontextmanager
async def get_chat_service():
    """Async context manager for using the ChatService"""
    await chat_service.initialize()
    yield chat_service


def rewrite_query(query: dict) -> str:
    """Inject retrieved content into prompt (if any)"""
    if query.get('search_results'):
        search = '\n'.join([f['title'] + f['text'] for f in query['search_results']])
        query['content'] = f"Based on the following search results:\n{search}\n\nQuestion: {query['content']}"
    elif query.get('files'):
        files = '\n'.join([f['file_content'] for f in query['files']])
        query['content'] = f"Based on the uploaded documents:\n{files}\n\nQuestion: {query['content']}"
    return query['content']


async def chat_generate(session_id: str, query: dict, kb_data: Union[dict, None]):
    """
    Async generator that streams AI responses using LangGraph and Ollama.
    """
    input_message = rewrite_query(query)

    async with get_chat_service() as service:
        state = {
            "messages": [input_message],
            "history": [],
            "kb_id": kb_data.get("kb_id", ""),
            "kb_name": kb_data.get("kb_name", ""),
            "kb_info": kb_data.get("kb_info", ""),
            "top_k": 5,
            "score_threshold": 0.7,
            "question": input_message,
            "docs": "",
            "retrieve_retry": 0,
        }

        async for msg in service.app.astream(state, stream_mode="messages"):
            if msg[1].get("langgraph_node") == "judge":
                continue
            if isinstance(msg[0], AIMessageChunk):
                yield msg[0].content
