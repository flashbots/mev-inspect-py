import os
from typing import Optional

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import sessionmaker


def get_trace_database_uri() -> Optional[str]:
    username = os.getenv("TRACE_DB_USER")
    password = os.getenv("TRACE_DB_PASSWORD")
    host = os.getenv("TRACE_DB_HOST")
    db_name = "trace_db"

    if all(field is not None for field in [username, password, host]):
        return f"postgresql+psycopg2://{username}:{password}@{host}/{db_name}"

    return None


def get_inspect_database_uri():
    username = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    db_name = "mev_inspect"
    return f"postgresql+psycopg2://{username}:{password}@{host}/{db_name}"


def _get_engine(uri: str):
    return create_engine(
        uri,
        executemany_mode="values",
        executemany_values_page_size=10000,
        executemany_batch_page_size=500,
    )


def _get_sessionmaker(uri: str):
    return sessionmaker(bind=_get_engine(uri))


def get_inspect_sessionmaker():
    uri = get_inspect_database_uri()
    return _get_sessionmaker(uri)


def get_trace_sessionmaker():
    uri = get_trace_database_uri()

    if uri is not None:
        return _get_sessionmaker(uri)

    return None


def get_inspect_session() -> orm.Session:
    Session = get_inspect_sessionmaker()
    return Session()


def get_trace_session() -> Optional[orm.Session]:
    Session = get_trace_sessionmaker()
    if Session is not None:
        return Session()

    return None
