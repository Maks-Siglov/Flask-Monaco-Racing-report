

from typing import Sequence

from sqlalchemy import (
    Row,
    select,
)

from app.db.session import s
from app.db.models.reports import (
    Driver,
    Result,
)


def report_query(order) -> Sequence[Driver]:
    """This function creates query for report router

    :param s: db session which we use in route to complete query
    :param order: sorting order if desc we order_by(...desc())
    :return: Sequence object which contains driver's abbr, name, team
    """
    statement = select(Driver)

    if order == 'desc':
        statement = select(Driver).order_by(Driver.abbr.desc())

    return s.user_db.scalars(statement)


def drivers_query(order) -> Sequence[Row[tuple[Result, Driver]]]:
    """This function creates query for drivers router

    :return: Sequence of rows with tuples which contains two object,
     first - Result with results data, second - Driver to whom result belongs
      with his abbr, team and name
    """
    statement = select(Result, Driver).join(Driver).order_by(Result.position)

    if order == 'desc':
        statement = select(Result, Driver).join(Driver).order_by(
            Result.position.desc())

    return s.user_db.execute(statement).all()


def unique_driver_query(driver_id) -> Row[tuple[Result, Driver]] | None:
    """This function creates query for unique driver router

    :param s: db session which we use in route to complete query
    :param driver_id: driver abbreviation
    :return: tuple which contains two object, first - Result with
    results data, second - Driver or None if driver_id (abbr) don't exist in db
    """
    statement =(
        select(Result, Driver)
        .join(Driver)
        .where(Driver.abbr == driver_id)
    )

    return s.user_db.execute(statement).one_or_none()
