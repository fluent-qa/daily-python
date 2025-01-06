from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from enum import Enum

from sqlalchemy import Delete, Insert, Update, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session

from revisited_lessons.r_config.models import AppConfig, appConfig

session_context: ContextVar[str] = ContextVar("session_context")
read_engine = create_engine(str(appConfig.READER_DB_URL))


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


class EngineType(Enum):
    WRITER = "writer"
    READER = "reader"


def create_engines(config: AppConfig) -> dict[EngineType, AsyncEngine]:
    return {
        EngineType.WRITER: create_async_engine(config.WRITER_DB_URL, pool_recycle=3600),
        EngineType.READER: create_async_engine(config.READER_DB_URL, pool_recycle=3600),
    }


class RoutingSession(Session):
    def __init__(self, engines: dict[EngineType, AsyncEngine]):
        super().__init__()
        self.engines = engines

    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return self.engines[EngineType.WRITER].sync_engine
        else:
            return self.engines[EngineType.READER].sync_engine


_async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
)
session = async_scoped_session(
    session_factory=_async_session_factory,
    scopefunc=get_session_context,
)


class Base(DeclarativeBase): ...


@asynccontextmanager
async def session_factory() -> AsyncGenerator[AsyncSession, None]:
    _session = async_sessionmaker(
        class_=AsyncSession,
        sync_session_class=RoutingSession,
        expire_on_commit=False,
    )()
    try:
        yield _session
    finally:
        await _session.close()
