from sqlalchemy.orm import Session, sessionmaker

from app.db.models.base import Base
from app.db.config import engine


def create_table() -> None:
    """This function creates tables in database"""
    Base.metadata.create_all(engine)


def drop_table() -> None:
    """This function drops tables in database"""
    Base.metadata.drop_all(engine)


def get_session() -> Session:
    """This function create a session"""
    session = sessionmaker(engine)
    return session()
