import click
import os

from app.bl.report.console_view import build_from_parser
from app.db.engine import drop_database
from app.config import DB_NAME, DB_PATH
from app.bl.report.prepare import prepare_db

FOLDER_DATA = r'app/bl/data'


@click.group()
def cli():
    pass


@cli.command()
@click.option('--files', default=FOLDER_DATA, help='Path to the dir with logs')
@click.option('--driver', help='Shows statistic about driver ')
@click.option('--desc', is_flag=True, default=False, help='Descending order')
def report(files, driver, desc):
    """This function collecting argument for command line

    :return: arguments for build parser
    """
    if not os.path.exists(files):
        raise ValueError(f"Path {files} from --file argument don't exist")
    build_from_parser(files, driver, desc)


@cli.command()
@click.option('--db_name', default=DB_NAME, help='Name of the database')
@click.option('--drop', is_flag=True, help='Drop database')
@click.option('--load', is_flag=True, help='Insert data to the database')
def db(db_name, drop, load):
    if drop:
        return drop_database(DB_PATH, db_name)

    if load:
        prepare_db()


if __name__ == '__main__':
    cli()
