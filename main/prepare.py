from main.utils.utils import format_timedelta
from main.utils.provider import read_log_files
from datetime import datetime
import re

PATTERN = re.compile(r'(^[A-Z]+)(\S+)')
DATE_FORMAT = '%Y-%m-%d_%H:%M:%S.%f'
FOLDER_DATA = r'.\data'


def prepare(folder_path: str = FOLDER_DATA) -> list[int,
tuple[str, str, tuple[int, float], str]]:
    """This function prepare data for web application

    :return: data which used for creating web application
    """

    start_log, end_log, abbreviations_data = read_log_files(folder_path)
    prepared_data = prepare_data(start_log, end_log, abbreviations_data)
    prepared_data.sort(key=lambda x: x[2])
    prepared_data = list(enumerate(prepared_data, start=1))

    return prepared_data


def prepare_data(start_log: str, end_log: str, abbreviations_data: str) -> list[int,
tuple[str, str,tuple[int, float], str]]:
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
