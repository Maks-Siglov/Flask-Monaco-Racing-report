import pytest

from app.config import BASE_URL, DB_NAME
from app.db.engine import create_database_or_engine
from app.db.session import set_session, pop_session, s
from app.db.utils import create_table, drop_table


@pytest.fixture(scope='session')
def create_test_db():
    engine = create_database_or_engine(BASE_URL, DB_NAME, {})
    create_table(engine)
    yield engine
    drop_table(engine)
    engine.dispose()

@pytest.fixture
def fresh_db(create_test_db):
    drop_table(create_test_db)
    create_test_db.dispose()

    engine = create_database_or_engine(BASE_URL, DB_NAME, {})
    create_table(engine)
    yield engine
    drop_table(engine)
    engine.dispose()


@pytest.fixture
def test_session():
    set_session()
    yield s
    pop_session()
