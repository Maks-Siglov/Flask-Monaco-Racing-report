import logging

from sqlalchemy import create_engine, text, Engine
from sqlalchemy.orm import Session, sessionmaker
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
        log.error(f'Creating database {db_name}')

    return create_engine(f'{db_url}/{db_name}', **options)


def _create_database(db_url: str, db_name: str) -> None:
    """This function creates database by db_url and db_name"""
    with create_engine(db_url).begin() as connect:
        connect.execute(text(f'CREATE DATABASE {db_name}'))


engine = create_database_or_engine(BASE_URL, DB_NAME, ENGINE_OPTIONS)


def get_session(db_engine: Engine = engine) -> Session:
    """This function create a session"""
    session = sessionmaker(db_engine)
    return session()


def check_db(db_engine: Engine = engine) -> None:
    """This function open and close check connection to db and make test session
    query before app running to display log information to ensure that db work
    as expected"""
    try:
        connect = db_engine.connect()
        log.error(f'Database ready: {not connect.closed}')
        with get_session(db_engine) as session:
            session.scalars(text('SELECT 1'))
        connect.close()
        log.error(f'Check connection close: {connect.closed}')
    except Exception as e:
        log.error(f'Database connection error: {str(e)}')

