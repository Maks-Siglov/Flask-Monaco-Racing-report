import os

START_LOG = 'start.log'
END_LOG = 'end.log'
ABBREVIATIONS = 'abbreviations.txt'


def read_log_files(folder_path) -> tuple[list[str]]:
    """This function use read_file() and return data from files

    :return: function returns data from .log files and abbreviations.txt
    """

    start_log = read_file(folder_path, START_LOG)
    end_log = read_file(folder_path, END_LOG)
    abbreviations_data = read_file(folder_path, ABBREVIATIONS)
    return start_log, end_log, abbreviations_data


def read_file(folder_path, filename) -> list[str] | None:
    """This function take filename and return data for it

    :param filename: name of file in data dir which contains data
    :param folder_path: path to the data folder
    :return: list with data from file
    """

    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            result = f.read().splitlines()

        return result

    else:
        print(f"Path {folder_path} don't exist")
        return None


def format_timedelta(timedelta_obj) -> tuple[int, float]:
    """This function convert timedelta object into tuple with numbers for report

    :param timedelta_obj: timedelta result of subtraction of time of end lap and start lap
    :return: tuple with minutes and seconds (int and float)
    """
    minute, seconds = divmod(timedelta_obj.total_seconds(), 60)

    return int(minute), round(seconds, 3)
