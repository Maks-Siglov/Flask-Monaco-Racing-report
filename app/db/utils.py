from sqlalchemy import Engine

from app.db.models.base import Base
from app.db.session import engine


def create_table(db_engine: Engine = engine) -> None:
    """This function creates tables in database"""
    Base.metadata.create_all(db_engine)


def drop_table(db_engine: Engine = engine) -> None:
    """This function drops tables in database"""
    Base.metadata.drop_all(db_engine)
