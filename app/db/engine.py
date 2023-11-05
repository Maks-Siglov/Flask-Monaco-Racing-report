

import logging

from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

from app.config import BASE_URL, DB_NAME, ENGINE_OPTIONS

log = logging.getLogger(__name__)


def create_database(db_url: str, db_name: str) -> None:
    """This function creates database by db_url and db_name"""
    try:
        with create_engine(
                db_url, isolation_level='AUTOCOMMIT'
        ).begin() as connect:
            connect.execute(text(f'CREATE DATABASE {db_name}'))
            log.warning(f'Database {db_name} was CREATED')
    except ProgrammingError:
        log.error(f'Database {db_name} already Exists')


def drop_database(db_url: str, db_name: str) -> None:
    """This function drops database by db_url and db_name"""
    try:
        with create_engine(
                db_url, isolation_level='AUTOCOMMIT'
        ).begin() as connect:
            connect.execute(text(f'DROP DATABASE {db_name} WITH(FORCE)'))
            log.warning(f'Database {db_name} was DROPPED')
    except ProgrammingError:
        log.error(f"Database {db_name} don't exist")


engine = create_engine(f'{BASE_URL}/{DB_NAME}', **ENGINE_OPTIONS)
