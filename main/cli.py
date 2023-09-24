from report import build_report, print_report, report_unique_driver
from utils import read_log_files
import argparse
import os


def start_parser() -> tuple[str, str | None, bool]:
    """This function collecting argument for command line

    :return: arguments for build parser
    """

    parser = argparse.ArgumentParser(prog='Report_CLI', description='CLI for report')

    parser.add_argument('--files', default='../data/', help='Give a path to the dir with logs file')
    parser.add_argument('--asc', action='store_true',  help='Sort in ascending order.')
    parser.add_argument('--desc', action='store_true', help='Sort in descending order.')
    parser.add_argument('--driver', help='Shows statistic about driver ')

    args = parser.parse_args()

    if not os.path.exists(args.files):
        raise ValueError("Path from --file argument don't exist")

    return args.files, args.driver, args.desc


def build_parser(args_files: str, args_driver: str, args_desc: bool) -> None:
    """This function build the parser

    :param args_files: path to the data folder, argument from start_parser()
    :param args_driver: name of the driver about whom we show the statistic, if None we don't show
    :param args_desc: order in which we show drivers statistic, if True order-descending, if False order-ascending
    """

    if args_files:
        start_log, end_log, abbreviations_data = read_log_files(args_files)
        prepared_data = build_report(start_log, end_log, abbreviations_data)
        prepared_data.sort(key=lambda x: x[2])
        prepared_data = list(enumerate(prepared_data, start=1))

    if args_driver:
        report_unique_driver(args_driver, prepared_data)

    if args_desc is False and args_driver is None:
        print_report(prepared_data)

    if args_desc is True:
        prepared_data.reverse()
        print_report(prepared_data, 15)


if __name__ == '__main__':
    args_files, args_driver, args_desc = start_parser()
    build_parser(args_files, args_driver, args_desc)
