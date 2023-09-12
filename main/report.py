from datetime import datetime
from main.utils import format_timedelta


class Report:                                                                   
    """This class takes data from .log files, prepare it and build report

        :param start_log: data about start time lap from log file
        :param end_log: data about end time lap from log file
        :param abbreviations_data: data from file contains abbreviation explanations
        """

    def __init__(self, start_log, end_log, abbreviations_data):
        self.start_log = start_log
        self.end_log = end_log
        self.abbreviations_data = abbreviations_data

    @staticmethod
    def build_data(file) -> dict:
        """This method takes data for file

        :param file: file where we take data
        :return: dictionary, where abbreviation is key, start lap time - is value
        """

        prepare_result = {}

        for param in file:
            abbreviation, date_obj = param.strip().split('2018-05-24_12:')
            date_obj = datetime.strptime(date_obj, '%M:%S.%f')
            prepare_result[abbreviation] = date_obj

        return prepare_result

    def build_report(self) -> list:
        """This method prepare data for print_report()
        :return: data for building (printing) report
        """

        prepare_start = self.build_data(self.start_log)
        prepare_end = self.build_data(self.end_log)

        prepared_data = []

        for param in self.abbreviations_data:
            abv, name, team = param.strip().split('_')
            lap_time = format_timedelta(prepare_end[abv] - prepare_start[abv])
            prepared_data.append((name, team, lap_time, abv))

        return prepared_data

    @staticmethod
    def print_report(prepared_data, index_underline=16) -> None:
        """This method build (print) report

        :param prepared_data: list with prepared data for report from build_report()
        :param index_underline: it is index where we print underline for drivers that has worst time lap, it can change
        if we use descending ordering
        """

        for index, item in prepared_data:
            name, team, lap_time, _ = item
            minutes, seconds = lap_time
            string_index = f'{str(index)}.'
            row = f'{string_index:<3} {name:<18} | {team:<26} | {minutes}:{seconds}'

            if index != index_underline:
                print(row)

            else:
                print('-' * 62)
                print(row)

    @staticmethod
    def report_unique_driver(driver_name, prepared_data) -> None:
        """This function build (print) report about unique driver

        :param driver_name:
        :param prepared_data:
        """

        for index, item in prepared_data:
            name, team, lap_time, _ = item
            minutes, seconds = lap_time
            if driver_name == name:
                print(f'{index}. {name} | {team} | {minutes}:{seconds}')
