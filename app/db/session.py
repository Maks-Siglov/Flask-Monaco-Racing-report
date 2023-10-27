import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import BASE_URL, DB_NAME, ENGINE_OPTIONS

log = logging.getLogger(__name__)

engine = create_engine(f'{BASE_URL}/{DB_NAME}', **ENGINE_OPTIONS)


def get_session() -> Session:
    """This function create a session"""
    session = sessionmaker(engine)
    return session()


def check_db():
    """This function open and close check connection to db before app
     running to display log information to ensure that db work as expected"""
    connect = engine.connect()
    log.error(f'Database ready: {not connect.closed}')
    connect.close()
    log.error(f'Check connection close: {connect.closed}')
