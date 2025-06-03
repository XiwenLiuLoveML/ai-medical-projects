# 🧠 Chat Module (LLM-Powered Medical Q&A)

This module provides the base chat interface using Ollama + LangGraph.
It supports streamed replies for medical Q&A powered by Retrieval-Augmented Generation (RAG).

## Key Components

- `chat.py`: Main logic for chat generation
- `ChatService`: Handles LangGraph compilation and singleton setup
- `chat_generate`: Async streaming generator for conversation
- `rewrite_query`: Enriches prompts using uploaded files or search results

## Dependencies

- `langgraph`
- `langchain_ollama`
- `ollama` endpoint
- Custom: `gen_rag_graph` from `agent/rag_agent.py`
