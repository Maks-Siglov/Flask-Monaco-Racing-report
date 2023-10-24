import pytest
from peewee import SqliteDatabase

from app.app import app
from app.db.models import BaseModel, Driver, Result


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_db():
    test_db = SqliteDatabase(':memory:')
    test_db.connect()
    BaseModel._meta.database = test_db
    test_db.create_tables([Driver, Result])
    yield test_db
    test_db.drop_tables([Driver, Result])
    test_db.close()
