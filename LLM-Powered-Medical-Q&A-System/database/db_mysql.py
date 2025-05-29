# db_mysql.py
# -----------------------------------------
# 📁 Description:
# Initializes the async and sync MySQL engines and sessions for the app.
# Provides:
# - AsyncSession for use in FastAPI
# - SyncSession for migrations or scripts
# - Table creation helper
# - UUID generator for primary keys
# -----------------------------------------

from typing import Annotated, AsyncGenerator
from uuid import uuid4
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi import Depends

from config.settings import settings
from common.model import MappedBase


def create_engine_and_session(url: str):
    engine = create_async_engine(url, echo=settings.MYSQL_ECHO, future=True, pool_pre_ping=True)
    db_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    return engine, db_session


# Async engine (for FastAPI)
SQLALCHEMY_DATABASE_URL = (
    f'mysql+asyncmy://{settings.MYSQL_USER}:{quote_plus(settings.MYSQL_PASSWORD)}@{settings.MYSQL_HOST}:'
    f'{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}?charset={settings.MYSQL_CHARSET}'
)
async_engine, async_db_session = create_engine_and_session(SQLALCHEMY_DATABASE_URL)

# Sync engine (for Alembic or admin scripts)
SQLALCHEMY_DATABASE_URL = (
    f'mysql+pymysql://{settings.MYSQL_USER}:{quote_plus(settings.MYSQL_PASSWORD)}@{settings.MYSQL_HOST}:'
    f'{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}?charset={settings.MYSQL_CHARSET}'
)
sync_engine = create_engine(SQLALCHEMY_DATABASE_URL)
SyncSession = sessionmaker(sync_engine)


# Dependency for FastAPI routes
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_db_session() as current_db:
        yield current_db


CurrentSession = Annotated[AsyncSession, Depends(get_db)]


async def create_table():
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)


def uuid4_str() -> str:
    return str(uuid4())
