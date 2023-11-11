

from typing import Sequence

from sqlalchemy import (
    Row,
    select,
)

from app.db.session import s
from app.db.models.result import Result
from app.db.models.driver import Driver


def report_query(order) -> Sequence[Driver]:
    """This function creates query for report router

    :param order: sorting order if desc we order_by(...desc())
    :return: list which contains driver's abbr, name, team
    """
    if order == 'desc':
        ordering = Driver.abbr.desc()
    else:
        ordering = Driver.abbr.asc()

    statement = select(Driver).order_by(ordering)

    return s.user_db.scalars(statement).all()


def drivers_query(order) -> Sequence[Row[tuple[Result, Driver]]]:
    """This function creates query for drivers router

    :return: Sequence of rows with tuples which contains two object,
    first - Result with results data, second - Driver to whom result belongs
    with his abbr, team and name
    """
    if order == 'desc':
        ordering = Result.position.desc()
    else:
        ordering = Result.position.asc()

    statement = select(Result, Driver).join(Driver).order_by(ordering)

    return s.user_db.execute(statement).all()


def unique_driver_query(driver_id) -> Row[tuple[Result, Driver]] | None:
    """This function creates query for unique driver router

    :param driver_id: driver abbreviation
    :return: Row with tuple which contains two object, first - Result with
    results data, second - Driver or None if driver_id (abbr) don't exist in db
    """
    statement = (
        select(Result, Driver)
        .join(Driver)
        .where(Driver.abbr == driver_id)
    )

    return s.user_db.execute(statement).first()
