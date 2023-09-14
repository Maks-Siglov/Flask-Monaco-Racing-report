from report import build_report, print_report, report_unique_driver
from utils import read_log_files
import argparse


def start_parser():
    """This function collecting argument for command line

    :return: arguments for build parser
    """

    parser = argparse.ArgumentParser(prog='Report_CLI', description='CLI for report')

    parser.add_argument('--files', default='../data/', help='Give a path to the dir with logs file')
    parser.add_argument('--asc', action='store_true',  help='Sort in ascending order.')
    parser.add_argument('--desc', action='store_true', help='Sort in descending order.')
    parser.add_argument('--driver', help='Shows statistic about driver ')

    args = parser.parse_args()

    return args


def build_parser(args):
    """This function build the parser

    :param args: arguments from start_parser() with which we build parser
    """

    if args.files:
        start_log, end_log, abbreviations_data = read_log_files(args.files)
        prepared_data = build_report(start_log, end_log, abbreviations_data)
        prepared_data.sort(key=lambda x: x[2])
        prepared_data = list(enumerate(prepared_data, start=1))

    if args.asc:
        print_report(prepared_data)

    if args.desc:
        prepared_data.reverse()
        print_report(prepared_data, 15)

    if args.driver:
        report_unique_driver(args.driver, prepared_data)


if __name__ == '__main__':
    parser = start_parser()
    build_parser(parser)
