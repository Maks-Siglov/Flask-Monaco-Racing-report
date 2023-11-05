

from app.db.models.base import Base
from app.db.session import s


def create_table() -> None:
    """This function creates tables in database"""
    Base.metadata.create_all(s.user_db.get_bind())


def drop_table() -> None:
    """This function drops tables in database"""
    Base.metadata.drop_all(s.user_db.get_bind())
