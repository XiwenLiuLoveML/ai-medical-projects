# app/admin/api/llm.py — Core API endpoints for medical LLM Q&A demo

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio

router = APIRouter()

# 🧠 Simple chat input schema
class ChatRequest(BaseModel):
    question: str
    session_id: str

# 📩 Multi-turn chat simulation (non-streaming)
@router.post("/chat/completion")
async def chat_completion(data: ChatRequest):
    """Simulate LLM generating a response to a user question."""
    return {
        "session_id": data.session_id,
        "question": data.question,
        "answer": "This is a demo response from the medical assistant."
    }

# 🌊 Streaming chat generation via SSE
@router.get("/generate")
async def generate_stream():
    """Stream generated tokens one by one using SSE (for demo)."""

    async def event_generator():
        words = ["This", "is", "a", "real-time", "response", "streamed", "by", "LLM."]
        for word in words:
            await asyncio.sleep(0.3)
            yield f"data: {word} \n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
