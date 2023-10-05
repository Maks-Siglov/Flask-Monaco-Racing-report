import os

START_LOG = 'start.log'
END_LOG = 'end.log'
ABBREVIATIONS = 'abbreviations.txt'


def read_log_files(folder_path: str) -> tuple[list[str], list[str], list[str]]:
    """This function use read_file() and return data from files

    :return: function returns data from .log files and abbreviations.txt
    """

    start_log = _read_file(folder_path, START_LOG)
    end_log = _read_file(folder_path, END_LOG)
    abbreviations_data = _read_file(folder_path, ABBREVIATIONS)
    return start_log, end_log, abbreviations_data


def _read_file(folder_path: str, filename: str) -> list[str]:
    """This function take filename and return data for it

    :param filename: name of file in data dir which contains data
    :param folder_path: path to the data folder
    :return: list with data from file
    """

    file_path = os.path.join(folder_path, filename)
    if not os.path.isfile(file_path):
        raise ValueError(f"Path {file_path} don't exist")
    with open(file_path, 'r') as f:
        result = f.read().splitlines()
    return result
