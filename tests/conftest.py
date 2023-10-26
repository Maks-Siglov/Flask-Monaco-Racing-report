import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.app import app
from app.db.models.reports import Base


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    session = session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()
