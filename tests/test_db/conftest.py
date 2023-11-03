import pytest

from app.config import BASE_URL, DB_NAME
from app.db.engine import create_database_or_engine
from app.db.session import set_session, close_dbs, s
from app.db.utils import create_table, drop_table


@pytest.fixture(scope='session')
def create_test_db():
    engine = create_database_or_engine(BASE_URL, DB_NAME, {})
    create_table(engine)
    yield engine
    drop_table(engine)
    engine.dispose()


@pytest.fixture
def test_session():
    set_session()
    yield s
    close_dbs()


@pytest.fixture()
def clean_up_database(create_test_db):
    drop_table(create_test_db)
    create_table(create_test_db)
