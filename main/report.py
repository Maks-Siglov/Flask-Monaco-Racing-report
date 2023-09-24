from datetime import datetime
from utils import format_timedelta
from typing import List, Tuple


SEPARATOR_SYMBOL = '-'
SEPARATOR_LENGTH = 62
INDEX_INDENT = 3
NAME_INDENT = 18
TEAM_INDENT = 26
INDEX_UNDERLINE = 16


def build_report(start_log: dict, end_log: dict,
                 abbreviations_data: list) -> list[int, tuple[str, str, tuple[int, float], str]]:
    """This function prepare data for print_report()

    :param start_log: data about start time lap from log file
    :param end_log: data about end time lap from log file
    :param abbreviations_data: data from file contains abbreviation explanations
    :return: data for building (printing) report
    """
    prepare_start = build_data(start_log)
    prepare_end = build_data(end_log)

    prepared_data = []

    for param in abbreviations_data:
        abv, name, team = param.strip().split('_')
        lap_time = format_timedelta(prepare_end[abv] - prepare_start[abv])
        prepared_data.append((name, team, lap_time, abv))

    return prepared_data


def build_data(file_name: str) -> dict[str, datetime]:
    """This function takes data for file

    :param file_name: file where we take data
    :return: dictionary, where abbreviation is key, start lap time - is value
    """

    prepare_result = {}

    for param in file_name:
        abbreviation, date_obj = param.strip().split('2018-05-24_12:')
        date_obj = datetime.strptime(date_obj, '%M:%S.%f')
        prepare_result[abbreviation] = date_obj

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
