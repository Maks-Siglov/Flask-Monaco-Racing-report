from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DB_PATH = 'app/db/report.db'
DB_URL = f'sqlite:///{DB_PATH}'

engine = create_engine(DB_URL)


def get_session() -> Session:
    """This function create a session"""
    session = sessionmaker(engine)
    return session()
