import os


class ReaderFiles:
    """This class provide functionality for reading data from log files for report"""
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def read_file(self, filename) -> list:
        """This method take filename and return data for it

        :param filename: name of file in data dir which contains data
        :return: list with data from file
        """

        file_path = os.path.join(self.folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                result = f.readlines()

            return result

        else:
            print(f"Path {self.folder_path} don't exist")
            return None

    def read_log_files(self) -> tuple:
        """This method use read_file() and return data from files

        :return: method returns data from .log files and abbreviations.txt
        """

        start_log = self.read_file('start.log')
        end_log = self.read_file('end.log')
        abbreviations_data = self.read_file('abbreviations.txt')
        return start_log, end_log, abbreviations_data


def format_timedelta(timedelta_obj) -> tuple:
    """This function convert timedelta object into tuple with numbers for report

    :param timedelta_obj: timedelta result of subtraction of time of end lap and start lap
    :return: tuple with minutes and seconds (int and float)
    """
    minute, seconds = divmod(timedelta_obj.total_seconds(), 60)

    return int(minute), round(seconds, 3)
