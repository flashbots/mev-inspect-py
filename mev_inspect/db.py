import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    return create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))


def get_session():
    Session = sessionmaker(bind=get_engine())
    return Session()
