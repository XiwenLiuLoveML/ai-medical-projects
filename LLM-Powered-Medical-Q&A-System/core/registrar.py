# core/registrar.py — Register app modules: logging, middleware, routers, exceptions

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.router import route

def register_app() -> FastAPI:
    """Create and configure FastAPI app."""
    app = FastAPI(
        title="Medical LLM QA System",
        description="A demo FastAPI backend for healthcare chatbot",
        version="0.1.0"
    )

    register_router(app)
    register_pagination(app)

    return app

def register_router(app: FastAPI):
    """Attach API routers to app."""
    app.include_router(route)

def register_pagination(app: FastAPI):
    """Enable pagination in API responses."""
    add_pagination(app)
