import pytest

from app.config import TEST_BASE_URL, TEST_DB_NAME
from app.db.session import create_database_or_engine, get_session
from app.db.utils import create_table, drop_table


@pytest.fixture(scope='session')
def create_test_db():
    engine = create_database_or_engine(TEST_BASE_URL, TEST_DB_NAME, {})
    create_table(engine)
    yield engine
    drop_table(engine)
    engine.dispose()


@pytest.fixture
def test_db_session(create_test_db):
    session = get_session(create_test_db)
    yield session
    session.close()
