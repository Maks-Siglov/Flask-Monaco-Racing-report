from main.report import build_from_parser
import argparse
import os


def start_parser() -> tuple[str, str | None, bool]:
    """This function collecting argument for command line

    :return: arguments for build parser
    """
    FOLDER_DATA = r'.\data'

    parser = argparse.ArgumentParser(prog='Report_CLI',
                                     description='CLI for report')

    parser.add_argument(
                        '--files',
                        default=FOLDER_DATA,
                        help='Give a path to the dir with logs file'
                        )
    parser.add_argument(
                        '--asc',
                        action='store_true',
                        help='Sort in ascending order.'
                        )
    parser.add_argument(
                        '--desc',
                        action='store_true'
                        , help='Sort in descending order.'
                        )
    parser.add_argument(
                        '--driver',
                        help='Shows statistic about driver '
                        )

    args = parser.parse_args()

    if not os.path.exists(args.files):
        raise ValueError(f"Path {args.files} from --file argument don't exist")

    return args.files, args.driver, args.desc


if __name__ == '__main__':
    args_files, args_driver, args_desc = start_parser()
    build_from_parser(args_files, args_driver, args_desc)
