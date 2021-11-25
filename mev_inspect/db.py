import os
from typing import Optional, Tuple
from asyncio import current_task

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_scoped_session,
)


def get_trace_database_uri() -> Optional[str]:
    username = os.getenv("TRACE_DB_USER")
    password = os.getenv("TRACE_DB_PASSWORD")
    host = os.getenv("TRACE_DB_HOST")
    db_name = "trace_db"

    if all(field is not None for field in [username, password, host]):
        return f"postgresql+asyncpg://{username}:{password}@{host}/{db_name}"

    return None


def get_inspect_database_uri():
    username = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    db_name = "mev_inspect"
    return f"postgresql+asyncpg://{username}:{password}@{host}/{db_name}"


def _get_engine(uri: str):
    return create_async_engine(uri)


def _get_session(uri: str):
    session = sessionmaker(bind=_get_engine(uri), class_=AsyncSession)
    return async_scoped_session(session, scopefunc=current_task)


def get_inspect_session() -> async_scoped_session:
    uri = get_inspect_database_uri()
    return _get_session(uri)


def get_trace_session() -> Optional[async_scoped_session]:
    uri = get_trace_database_uri()

    if uri is not None:
        return _get_session(uri)

    return None


def get_sessions() -> Tuple[async_scoped_session, Optional[async_scoped_session]]:
    inspect_db_session = get_inspect_session()
    trace_db_session = get_trace_session()
    trace_db_session = trace_db_session() if trace_db_session is not None else None
    return inspect_db_session, trace_db_session
