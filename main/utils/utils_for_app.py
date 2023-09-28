from main.cli import start_parser
from main.report import prepare_data
from .utils_for_report import read_log_files


def prepare() -> list[int, tuple[str, str, tuple[int, float], str]]:
    """This function prepare data for web application

    :return: data which used for creating web application
    """
    ARGS_FILES, ARGS_DRIVER, ARGS_DESC = start_parser()

    start_log, end_log, abbreviations_data = read_log_files(ARGS_FILES)
    prepared_data = prepare_data(start_log, end_log, abbreviations_data)
    prepared_data.sort(key=lambda x: x[2])
    prepared_data = list(enumerate(prepared_data, start=1))

    return prepared_data
