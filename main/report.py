from datetime import datetime
from main.utils.utils_for_report import read_log_files, format_timedelta
from typing import List, Tuple
import re

PATTERN = re.compile(r'(^[A-Z]+)(\S+)')
DATE_FORMAT = '%Y-%m-%d_%H:%M:%S.%f'

SEPARATOR_SYMBOL = '-'
SEPARATOR_LENGTH = 62
INDEX_INDENT = 3
NAME_INDENT = 18
TEAM_INDENT = 26
INDEX_UNDERLINE = 16


def build_from_parser(args_files: str, args_driver: str, args_desc: bool) -> None:
    """This function takes argument for parser and build report

    :param args_files: path to the data folder, argument from start_parser()
    :param args_driver: name of the driver about whom we show the statistic, if None we don't show
    :param args_desc: order in which we show drivers statistic, if True order-descending, if False order-ascending
    """

    if args_files:
        start_log, end_log, abbreviations_data = read_log_files(args_files)
        prepared_data = prepare_data(start_log, end_log, abbreviations_data)
        prepared_data.sort(key=lambda x: x[2])
        prepared_data = list(enumerate(prepared_data, start=1))

    if args_driver:
        report_unique_driver(args_driver, prepared_data)

    if args_desc is False and args_driver is None:
        print_report(prepared_data)

    if args_desc is True:
        prepared_data.reverse()
        index_underline = 15
        print_report(prepared_data, index_underline)


def prepare_data(start_log: list[str], end_log: list[str],
                 abbreviations_data: list) -> list[int, tuple[str, str, tuple[int, float], str]]:
    """This function prepare data for print_report()

    :param start_log: data about start time lap from log file
    :param end_log: data about end time lap from log file
    :param abbreviations_data: data from file contains abbreviation explanations
    :return: data for building (printing) report
    """
    prepare_start = prepare_data_from_file(start_log)
    prepare_end = prepare_data_from_file(end_log)

    prepared_data = []
    for param in abbreviations_data:
        abr, name, team = param.strip().split('_')
        lap_time = format_timedelta(prepare_end[abr] - prepare_start[abr])
        prepared_data.append((name, team, lap_time, abr))

    return prepared_data


def prepare_data_from_file(file_data: str) -> dict[str, datetime]:
    """This function takes data for file

    :param file_data: file where we take data
    :return: dictionary, where abbreviation is key, start lap time - is value
    """

    prepare_result = {}

    for param in file_data:
        match = PATTERN.match(param)
        abr, time = match.groups()
        prepare_result[abr] = datetime.strptime(time, DATE_FORMAT)

    return prepare_result


def print_report(prepared_data: List[Tuple[str, str, Tuple[int, float], str]],
                 index_underline: int = INDEX_UNDERLINE) -> None:
    """This function build (print) report

    :param prepared_data: list with prepared data for report from build_report()
    :param index_underline: it is index where we print underline for drivers that has worst time lap, it can change
    if we use descending ordering
    """

    for position, item in prepared_data:
        name, team, lap_time, _ = item
        minutes, seconds = lap_time
        string_position = f'{position}.'
        row = f'{string_position:<{INDEX_INDENT}} {name:<{NAME_INDENT}} | {team:<{TEAM_INDENT}} | {minutes}:{seconds}'

        if position != index_underline:
            print(row)

        else:
            print(SEPARATOR_SYMBOL * SEPARATOR_LENGTH)
            print(row)


def report_unique_driver(driver_name: str, prepared_data: List[Tuple[str, str, Tuple[int, float], str]]) -> None:
    """This function build (print) report about unique driver

    :param driver_name: name of the driver
    :param prepared_data: data for report
    """

    for position, item in prepared_data:
        name, team, lap_time, _ = item
        minutes, seconds = lap_time
        if driver_name == name:
            print(f'{position}. {name} | {team} | {minutes}:{seconds}')
