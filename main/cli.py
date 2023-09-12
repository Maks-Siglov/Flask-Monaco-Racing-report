from report import Report
from utils import ReaderFiles
import argparse


class Parser:
    """This class provide functionality for working with parser"""
    @staticmethod
    def start_parser():
        """This method collecting argument for command line

        :return: arguments for build parser
        """

        parser = argparse.ArgumentParser(prog='Report_CLI', description='CLI for report')

        parser.add_argument('--files', default='../data/', help='Give a path to the dir with logs file')
        parser.add_argument('--asc', action='store_true',  help='Sort in ascending order.')
        parser.add_argument('--desc', action='store_true', help='Sort in descending order.')
        parser.add_argument('--driver', help='Shows statistic about driver ')

        args = parser.parse_args()

        return args

    @staticmethod
    def build_parser(args):
        """This method build the parser

        :param args: arguments from start_parser() with which we build parser
        """

        if args.files:
            start_log, end_log, abbreviations_data = ReaderFiles(args.files).read_log_files()
            prepared_data = Report(start_log, end_log, abbreviations_data).build_report()
            prepared_data.sort(key=lambda x: x[2])                                               
            prepared_data = list(enumerate(prepared_data, start=1))

        if args.asc:
            Report.print_report(prepared_data)

        if args.desc:
            prepared_data.reverse()
            Report.print_report(prepared_data, 15)

        if args.driver:
            Report.report_unique_driver(args.driver, prepared_data)


if __name__ == '__main__':
    parser = Parser.start_parser()
    Parser.build_parser(parser)
