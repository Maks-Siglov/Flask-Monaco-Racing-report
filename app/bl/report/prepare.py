import re

from datetime import datetime
from sqlalchemy import func, select
from sqlalchemy.exc import OperationalError

from app.bl.report.utils.utils import format_timedelta
from app.bl.report.utils.provider import read_log_files
from app.db.models.reports import Driver, Result
from app.db.utils import create_table
from app.db.session import get_session

PATTERN = re.compile(r'(^[A-Z]+)(\S+)')
DATE_FORMAT = '%Y-%m-%d_%H:%M:%S.%f'
FOLDER_DATA = r'app/bl/data'


def prepare(folder_path: str = FOLDER_DATA
            ) -> list[Result]:
    """This function checks whether tables exist in the database and whether
     they contain data, if not, the tables are created and filled with data.
     Also function create PREPARED_DATA.

    :param folder_path: path to the folder with log files
    :return: list with result object which also contain data about driver and
     his results
    """
    with get_session() as session:
        try:
            session.execute(select(Driver)).all()
            session.execute(select(Result)).all()
        except OperationalError:
            create_table()
            _convert_and_store_data(folder_path)

        statement = select(Result).join(Result.driver).order_by(Result.position)

        return session.scalars(statement).all()


def _convert_and_store_data(folder_path) -> None:
    """This function convert data from log files and stores it to database

     :param folder_path: path to the folder with log files
     """
    start_log, end_log, abbreviations_data = read_log_files(folder_path)

    prepare_start = _prepare_data_from_file(start_log)
    prepare_end = _prepare_data_from_file(end_log)

    with get_session() as session:
        driver_results = []
        for param in abbreviations_data:
            abr, name, team = param.strip().split('_')
            minutes, seconds = format_timedelta(
                prepare_end[abr] - prepare_start[abr])

            driver = Driver(abr=abr, name=name, team=team)
            result = Result(owner=driver, minutes=minutes, seconds=seconds)
            driver_results.append(result)

        session.add_all(driver_results)
        sort_results(session)
        session.commit()


def _prepare_data_from_file(file_data: list[str]) -> dict[str, datetime]:
    """This function takes data from log file and prepare it

    :param file_data: file where we take data
    :return: dictionary, where abbreviation is key, start lap time - is value
    """

    prepare_result = {}

    for param in file_data:
        match = PATTERN.match(param)
        abr, time = match.groups()
        prepare_result[abr] = datetime.strptime(time, DATE_FORMAT)

    return prepare_result


def sort_results(session) -> None:
    """This function sorts results by his owner inside a database for and set
     position to each
    """
    statement = select(Result).order_by(
        Result.minutes < 0, func.ABS(Result.minutes) * 60 + Result.seconds)

    for pos, result in enumerate(session.execute(statement).scalars(), start=1):
        result.position = pos
