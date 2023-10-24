from app.db.config import db
from app.db.models import Driver, Result


def create_table() -> None:
    """This function creates tables in database"""
    with db:
        db.create_tables([Driver, Result])


def drop_table() -> None:
    """This function drops tables in database"""
    with db:
        db.drop_tables([Driver, Result])
