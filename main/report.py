from main.prepare import prepare

SEPARATOR_SYMBOL = '-'
SEPARATOR_LENGTH = 62
INDEX_INDENT = 3
NAME_INDENT = 18
TEAM_INDENT = 26
INDEX_UNDERLINE_ASC = 16
INDEX_UNDERLINE_DESC = 15


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


def print_report(
    prepared_data: list[tuple[int, tuple[str, str, tuple[int, float], str]]],
    order: bool = True
) -> None:
    """This function build (print) report

    :param prepared_data: list with prepared data for report from build_report()
    :param order: shows in which order report should be
    if we use descending ordering
    """
    if order:
        index_underline = INDEX_UNDERLINE_ASC
    else:
        index_underline = INDEX_UNDERLINE_DESC
        prepared_data.reverse()

    for position, item in prepared_data:
        name, team, lap_time, _ = item
        minutes, seconds = lap_time
        string_position = f'{position}.'
        row = f'{string_position:<{INDEX_INDENT}} {name:<{NAME_INDENT}}' \
              f' | {team:<{TEAM_INDENT}} | {minutes}:{seconds}'

        if position != index_underline:
            print(row)

        else:
            print(SEPARATOR_SYMBOL * SEPARATOR_LENGTH)
            print(row)


def report_unique_driver(
    prepared_data: list[tuple[int, tuple[str, str, tuple[int, float], str]]],
    driver_name: str
) -> None:
    """This function build (print) report about unique driver

    :param driver_name: name of the driver
    :param prepared_data: data for report
    """

    for position, item in prepared_data:
        name, team, lap_time, _ = item
        minutes, seconds = lap_time
        if driver_name == name:
            print(f'{position}. {name} | {team} | {minutes}:{seconds}')
