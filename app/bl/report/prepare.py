

import re

from datetime import datetime

from app.db.session import s
from app.bl.report.provider import read_log_files
from app.db.models import (
    Result,
    Driver,
    Team,
    Race,
    Stage,
)
from app.config import (
    FOLDER_DATA,
    RACE,
)


PATTERN = re.compile(r'(^[A-Z]+)(\S+)')
DATE_FORMAT = '%Y-%m-%d_%H:%M:%S.%f'


def convert_and_store_data(folder_path: str = FOLDER_DATA) -> None:
    """This function convert data from log files and stores it to database

    :param folder_path: path to the folder with log files
    """
    start_log, end_log, abbreviations_data = read_log_files(folder_path)

    prepare_start = _prepare_data_from_file(start_log)
    prepare_end = _prepare_data_from_file(end_log)
    race, stage = _prepare_race(RACE)

    teams = {}
    driver_results = []
    for param in abbreviations_data:
        abbr, name, team_name = param.strip().split('_')
        start, end = prepare_start[abbr], prepare_end[abbr]

        if team_name not in teams:
            teams[team_name] = Team(name=team_name)

        driver = Driver(abbr=abbr, name=name, team=teams[team_name])
        result = Result(
            driver=driver, race=race, stage=stage, start=start, end=end
        )
        driver_results.append(result)

    s.user_db.add_all(sort_results(driver_results))


def _prepare_data_from_file(file_data: list[str]) -> dict[str, datetime]:
    """This function takes data from log file and prepare it

    :param file_data: file where we take data
    :return: dictionary, where abbreviation is key, start lap time - is value
    """
    prepare_result = {}
    for param in file_data:
        match = PATTERN.match(param)
        assert match
        abbr, time = match.groups()
        prepare_result[abbr] = datetime.strptime(time, DATE_FORMAT)

    return prepare_result


def _prepare_race(race) -> tuple[Race, Stage]:
    """This function prepare Race and Stage model for report"""
    race_name, year, stage = race.strip().split('_')
    return Race(name=race_name, year=year), Stage(name=stage)


def sort_results(driver_results: list[Result]) -> list[Result]:
    """This function sorts results by his owner inside a database for and set
    position to each

    :return: List of sorted Result with position
    """
    sorted_result = sorted(
        driver_results,
        key=lambda item: (item.total_seconds < 0, abs(item.total_seconds))
    )

    for pos, result in enumerate(sorted_result, start=1):
        result.position = pos

    return sorted_result
