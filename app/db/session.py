

import logging

from dataclasses import dataclass
from contextvars import ContextVar
from sqlalchemy import (
    create_engine,
    Engine,
    select
)
from sqlalchemy.orm import (
    sessionmaker,
    Session,
    SessionTransaction
)

from app.config import (
    BASE_URL,
    DB_NAME,
    ENGINE_OPTIONS
)

log = logging.getLogger(__name__)


@dataclass
class EnginePool:
    engine: Engine
    maker: sessionmaker


session_pools: dict[str, EnginePool] = {}

user_db = ContextVar[Session]('user_db')
user_db_transaction = ContextVar[SessionTransaction | None](
    'user_db_transaction', default=None
)


class SessionExcept(Exception):
    pass


def set_session() -> None:
    """This function establish current EnginePool by get_pool_sync and set
    to the s.user_db sessionmaker of the current EnginePool"""
    current_pool = get_pool_sync(f'{BASE_URL}/{DB_NAME}', ENGINE_OPTIONS)
    s.user_db = current_pool.maker()
    s.user_db.connection(execution_options={'isolation_level': 'AUTOCOMMIT'})


def get_pool_sync(db_url: str, options: dict) -> EnginePool:
    """This function creates EnginePool dataclas which contains Engine and
    sessionmaker check connect, and set it  as a value to dict with db_url key

    :param db_url: url to database
    :param options: options for creating engine
    :return: EnginePool dataclass which contain Engine and sessionmaker
    """
    db_engine = session_pools.get(db_url)
    if not db_engine:
        auto_engine = create_engine(db_url, **options)
        _check_connection(auto_engine)
        auto_marker = _create_sessionmaker(auto_engine)

        db_engine = EnginePool(engine=auto_engine, maker=auto_marker)

        session_pools[db_url] = db_engine

    return db_engine


def _check_connection(engine: Engine) -> None:
    """This function check connection to engine created by the get_pool_sync"""
    try:
        with engine.connect() as conn:
            conn.execute(select(1))
            log.warning('Connection success')
    except Exception as e:
        log.error('During check connection error occurred')
        raise SessionExcept(e)


def _create_sessionmaker(engine: Engine) -> sessionmaker:
    """This function create sessionmaker for get_pool_sync"""
    return sessionmaker(bind=engine, expire_on_commit=False, future=True)


def pop_session() -> None:
    """This function should use after each request, it commits changes to db
    if exception occur make rollback and in each case close sessionmaker of
    the current EnginePool"""
    try:
        s.user_db.commit()
    except Exception as e:
        s.user_db.rollback()
        log.error(f'During session error occurred {str(e)}.Session ROLLBACK ')
    finally:
        s.user_db.close()


def close_dbs() -> None:
    """This function should use before app teardown it goes through each
    EnginePool which was created and dispose his engine"""
    for ses_pool in session_pools.values():
        ses_pool.engine.dispose()


class Sessions:
    @property
    def user_db(self) -> Session:
        return user_db.get()

    @user_db.setter
    def user_db(self, value: Session) -> None:
        user_db.set(value)

    @property
    def user_db_transaction(self) -> SessionTransaction | None:
        return user_db_transaction.get()

    @user_db_transaction.setter
    def user_db_transaction(self, value: SessionTransaction) -> None:
        user_db_transaction.set(value)


s = Sessions()
