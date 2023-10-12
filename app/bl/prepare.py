from app.bl.utils.utils import format_timedelta
from app.bl.utils.provider import read_log_files
from app.bl.models import Driver
from datetime import datetime
import re

PATTERN = re.compile(r'(^[A-Z]+)(\S+)')
DATE_FORMAT = '%Y-%m-%d_%H:%M:%S.%f'
FOLDER_DATA = r'app/bl/data'


def prepare(folder_path: str = FOLDER_DATA) -> list[Driver]:
    """This function prepare data for web application and report

    :return: data which used for creating web application
    """

    start_log, end_log, abbreviations_data = read_log_files(folder_path)
    driver_data = _prepare_data(start_log, end_log, abbreviations_data)
    drivers = sorted(driver_data.values())

    for position, item in enumerate(drivers, start=1):
        item.position = position

    return drivers


def _prepare_data(start_log: list[str], end_log: list[str],
                  abbreviations_data: list[str]) -> dict[str, Driver]:
    """This function prepare data for prepare()

    :param start_log: data about start time lap from log file
    :param end_log: data about end time lap from log file
    :param abbreviations_data: data from file contains abbreviation explanations
    :return: data for building (printing) report
    """
    prepare_start = _prepare_data_from_file(start_log)
    prepare_end = _prepare_data_from_file(end_log)

    driver_data = {}
    for param in abbreviations_data:
        abr, name, team = param.strip().split('_')
        lap_time = format_timedelta(prepare_end[abr] - prepare_start[abr])
        driver_data[abr] = Driver(
            abr=abr, name=name, team=team, lap_time=lap_time
        )

    return driver_data


def _prepare_data_from_file(file_data: list[str]) -> dict[str, datetime]:
    """This function takes data for file and prepare it

    :param file_data: file where we take data
    :return: dictionary, where abbreviation is key, start lap time - is value
    """

    prepare_result = {}

    for param in file_data:
        match = PATTERN.match(param)
        abr, time = match.groups()
        prepare_result[abr] = datetime.strptime(time, DATE_FORMAT)

    return prepare_result
