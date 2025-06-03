"""
📍 Path: backend/algorithms/llm/chat/analysis_chat.py

📌 This module allows users to upload patient Excel/CSV data and ask questions for automatic analysis.

It supports:
- AI-driven data exploration using LangGraph + Ollama
- Streaming thoughts, code, and results
- Chart generation (e.g., age distribution, recovery trends)
"""

import re
from typing import List, Union
from contextlib import asynccontextmanager
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessageChunk

from algorithms.llm.data_analysis.data_analysis import gen_analysis_graph, DataAnalysisState
from config.settings import settings


class AnalysisChatService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._app = None
        return cls._instance

    async def initialize(self):
        if self._app is None:
            ollama_chat = ChatOllama(
                base_url=settings.OLLAMA_API_URL,
                model='deepseek-r1:32b',
                temperature=0.8,
                num_predict=2560,
            )
            graph = gen_analysis_graph(ollama_chat)
            self._app = graph.compile()

    @property
    def app(self):
        if self._app is None:
            raise RuntimeError("AnalysisChatService not initialized")
        return self._app


analysis_chat_service = AnalysisChatService()


@asynccontextmanager
async def get_analysis_chat_service():
    await analysis_chat_service.initialize()
    yield analysis_chat_service


async def analysis_graph_generate(query: str, session_id: str, file_path: Union[str, List[str]]):
    async with get_analysis_chat_service() as service:
        config = {'configurable': {'thread_id': session_id}}
        state = DataAnalysisState(
            messages=HumanMessage(content=query),
            question=query,
            file_path=file_path,
            execution_result={}
        )
        try:
            content_type = 'text'
            code_flag = 1
            async for msg in service.app.astream(state, config, stream_mode='messages'):
                if msg[1].get("langgraph_node") == "judge":
                    continue
                if isinstance(msg[0], AIMessageChunk):
                    chunk = msg[0].content
                    if chunk.startswith('<think>'):
                        yield {'type': 'think', 'content': chunk[8:]}
                        continue
                    elif chunk.endswith('</think>'):
                        yield {'type': 'think', 'content': chunk[:-8]}
                        continue
                    if '```' in chunk:
                        code_flag += 1
                        yield {'type': 'code' if code_flag % 2 == 0 else 'text', 'content': chunk.replace('```python', '').replace('```', '').strip()}
                        continue
                    yield {'type': content_type, 'content': chunk}

            final_state = await service.app.aget_state(config)
            if final_state.values['should_analysis']:
                result = final_state.values['execution_result']
                yield {'type': result['type'], 'content': result['value']}
        except Exception as e:
            yield {'type': 'text', 'content': f"Error: {str(e)}"}
