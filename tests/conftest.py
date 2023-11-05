

import pytest

from app.app import create_app
from app.config import (
    DB_NAME,
    BASE_URL,
    FOLDER_DATA,
)
from app.db.utils import (
    drop_table,
    create_table,
)
from app.db.engine import (
    drop_database,
    create_database,
)
from app.db.session import (
    close_dbs,
    pop_session,
    set_session,
)
from app.bl.report.prepare import convert_and_store_data


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    create_database(BASE_URL, DB_NAME)
    set_session()
    create_table()
    convert_and_store_data(FOLDER_DATA)
    pop_session()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    try:
        close_dbs()
    finally:
        print('\nClose DB')

    try:
        drop_database(BASE_URL, DB_NAME)
    finally:
        print(f'DROP DB {DB_NAME}')


@pytest.fixture
def fresh_db():
    set_session()
    drop_table()
    create_table()
    yield
    drop_table()
    create_table()
    convert_and_store_data(FOLDER_DATA)
    pop_session()
