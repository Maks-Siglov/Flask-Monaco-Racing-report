import logging

from sqlalchemy import create_engine, text, Engine
from sqlalchemy.exc import OperationalError

from app.config import BASE_URL, DB_NAME, ENGINE_OPTIONS

log = logging.getLogger(__name__)


def create_database_or_engine(db_url: str, db_name: str, options: dict
                              ) -> Engine:
    """This function tries to create db, if it not already exist, after return
     Engine"""
    try:
        _create_database(db_url, db_name)
    except OperationalError:
        log.warning(f'Creating database {db_name}')

    return create_engine(f'{db_url}/{db_name}', **options)


def _create_database(db_url: str, db_name: str) -> None:
    """This function creates database by db_url and db_name"""
    with create_engine(db_url).begin() as connect:
        connect.execute(text(f'CREATE DATABASE {db_name}'))


engine = create_database_or_engine(BASE_URL, DB_NAME, ENGINE_OPTIONS)
