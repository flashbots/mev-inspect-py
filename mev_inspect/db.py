import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    username = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    server = "postgresql"
    db_name = "mev_inspect"
    uri = f"postgresql://{username}:{password}@{server}/{db_name}"
    return create_engine(uri)


def get_session():
    Session = sessionmaker(bind=get_engine())
    return Session()
