import os
from typing import Any, Iterable, List, Optional

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import sessionmaker

from mev_inspect.text_io import StringIteratorIO


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
        executemany_mode="batch",
        executemany_values_page_size=10000,
        executemany_batch_page_size=10000,
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


def write_as_csv(
    db_session,
    table_name: str,
    items: Iterable[Iterable[Any]],
) -> None:
    csv_iterator = StringIteratorIO(
        ("|".join(map(_clean_csv_value, item)) + "\n" for item in items)
    )

    with db_session.connection().connection.cursor() as cursor:
        cursor.copy_from(csv_iterator, table_name, sep="|")


def _clean_csv_value(value: Optional[Any]) -> str:
    if value is None:
        return r"\N"
    return str(value).replace("\n", "\\n")


def to_postgres_list(values: List[Any]) -> str:
    if len(values) == 0:
        return "{}"

    return "{" + ",".join(map(str, values)) + "}"
