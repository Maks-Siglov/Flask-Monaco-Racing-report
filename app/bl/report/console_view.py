

from sqlalchemy import select

from app.db.session import s
from app.crud.report import drivers_query
from app.db.models.reports import (
    Driver,
    Result,
)


SEPARATOR_SYMBOL = '-'
SEPARATOR_LENGTH = 64
INDEX_INDENT = 3
NAME_INDENT = 18
TEAM_INDENT = 26
INDEX_UNDERLINE = 15


def build_from_parser(
        args_files: str, args_driver: str | None, args_desc: bool
) -> None:
    """This function takes argument for parser and build report

    :param args_files: path to the data folder, argument from start_parser()
    :param args_driver: name of the driver about whom we show the statistic,
    if None we don't show
    :param args_desc: order in which we show drivers statistic,
    if True order-descending, if False order-ascending
    """

    if args_driver is None:
        order = False if args_desc else True
        print_report(order)

    else:
        report_unique_driver(args_driver)


def print_report(order: bool = True) -> None:
    """This function build (print) report

    :param order: shows in which order report should be
    if we use descending ordering
    """

    index_underline = INDEX_UNDERLINE + int(order)
    if not order:
        order = 'desc'

    for result, driver in drivers_query(order):
        string_position = f'{result.position}.'

        row = (
            f'{string_position:<{INDEX_INDENT}}'
            f' {driver.name:<{NAME_INDENT}} | '
            f' {driver.team:<{TEAM_INDENT}} | '
            f'{result.result[0]}:{result.result[1]}'
        )

        if result.position != index_underline:
            print(row)

        else:
            print(SEPARATOR_SYMBOL * SEPARATOR_LENGTH)
            print(row)


def report_unique_driver(driver_name: str) -> None:
    """This function build (print) report about unique driver

    :param driver_name: name of the driver
    """
    statement = select(Result, Driver).join(Driver).where(
        Driver.name == driver_name)
    item = s.user_db.execute(statement).one_or_none()
    if item:
        result, driver = item
        print(
            f'{result.position}. {driver.name} | {driver.team} |'
            f' {result.result[0]}:{result.result[1]}'
        )
    else:
        print(f"Driver {driver_name} don't exist")
