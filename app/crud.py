from sqlalchemy import select, ScalarResult

from app.db.models.reports import Driver, Result


def report_query(session, order) -> ScalarResult:
    """This function creates query for report router

    :param session: db session which we use in route to complete query
    :param order: sorting order if desc we order_by(...desc())
    :return: ScalarResult object which contains driver's abr, name, team
    """
    statement = select(Driver)

    if order == 'desc':
        statement = select(Driver).order_by(Driver.abr.desc())

    return session.scalars(statement)


def drivers_query(session, order) -> list[tuple[Result, Driver]]:
    """This function creates query for drivers router

    :return: list with tuples which contains two object, first - Result with
    results data, second - Driver to whom result belongs with his abr, team and
    name
    """
    statement = select(Result, Driver).join(Driver).order_by(Result.position)

    if order == 'desc':
        statement = select(Result, Driver).join(Driver).order_by(
            Result.position.desc())

    return session.execute(statement).all()


def unique_driver_query(session, driver_id) -> None | tuple[Result, Driver]:
    """This function creates query for unique driver router

    :param driver_id: driver abbreviation
    :return: tuple which contains two object, first - Result with
    results data, second - Driver or None if driver_id (abr) don't exist in db
    """
    statement = select(Result, Driver).join(Driver).where(
        Driver.abr == driver_id)

    return session.execute(statement).one_or_none()
