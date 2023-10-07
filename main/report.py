from main.prepare import prepare
from main.models import Driver

SEPARATOR_SYMBOL = '-'
SEPARATOR_LENGTH = 62
INDEX_INDENT = 3
NAME_INDENT = 18
TEAM_INDENT = 26
INDEX_UNDERLINE = 15


def build_from_parser(args_files: str, args_driver: str,
                      args_desc: bool) -> None:
    """This function takes argument for parser and build report

    :param args_files: path to the data folder, argument from start_parser()
    :param args_driver: name of the driver about whom we show the statistic,
     if None we don't show
    :param args_desc: order in which we show drivers statistic,
     if True order-descending, if False order-ascending
    """

    prepared_data = prepare(args_files)

    if args_driver is None:
        order = False if args_desc else True
        print_report(prepared_data, order)

    else:
        report_unique_driver(prepared_data, args_driver)


def print_report(prepared_data: list[Driver], order: bool = True) -> None:
    """This function build (print) report

    :param prepared_data: list with prepared data for report from build_report()
    :param order: shows in which order report should be
    if we use descending ordering
    """
    index_underline = INDEX_UNDERLINE + int(order)
    if not order:
        prepared_data.reverse()

    for driver in prepared_data:
        string_position = f'{driver.position}.'
        row = (f'{string_position:<{INDEX_INDENT}} {driver.name:<{NAME_INDENT}}'
               f' {driver.team:<{TEAM_INDENT}} | '
               f'{driver.lap_time.minutes}:{driver.lap_time.seconds}')

        if driver.position != index_underline:
            print(row)

        else:
            print(SEPARATOR_SYMBOL * SEPARATOR_LENGTH)
            print(row)


def report_unique_driver(prepared_data: list[Driver], driver_name: str) -> None:
    """This function build (print) report about unique driver

    :param driver_name: name of the driver
    :param prepared_data: data for report
    """

    for driver in prepared_data:
        if driver_name == driver.name:
            print(f'{driver.position}. {driver.name} | {driver.team} |'
                  f' {driver.lap_time.minutes}:{driver.lap_time.seconds}')
