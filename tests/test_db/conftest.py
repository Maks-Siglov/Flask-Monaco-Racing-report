import pytest

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.db.models.reports import Base
from app.config import TEST_BASE_URL, TEST_DB_NAME


@pytest.fixture
def test_db_session():
    engine = create_engine(f'{TEST_BASE_URL}/{TEST_DB_NAME}')
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    session = session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()
