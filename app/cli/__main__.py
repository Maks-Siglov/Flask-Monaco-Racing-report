import click
import os

from app.bl.report.console_view import build_from_parser
from app.db.engine import create_database_or_engine, drop_database
from app.config import DB_NAME, BASE_URL, ENGINE_OPTIONS
from app.bl.report.prepare import prepare_db

FOLDER_DATA = r'app/bl/data'


@click.group()
def cli() -> None:
    """This click cli group provides two commands first - report which represent
    at console report in desirable order or report about unique driver, the
    second provide interaction with database: create, drop, recreate and insert
    data to db. If you want report console view use report command, if you want
     to interact with database use db command.
    """
    pass


@cli.command()
@click.option('--files', default=FOLDER_DATA, help='Path to the dir with logs')
@click.option('--driver', help='Shows statistic about driver ')
@click.option('--desc', is_flag=True, default=False, help='Descending order')
def report(files: str, driver: str, desc: bool) -> None:
    if not os.path.exists(files):
        raise ValueError(f"Path {files} from --file argument don't exist")
    build_from_parser(files, driver, desc)


@cli.command()
@click.option('--db_name', default=DB_NAME, help='Name of the database')
@click.option('--create', is_flag=True, help='Create database')
@click.option('--drop', is_flag=True, help='Drop database')
@click.option('--recreate', is_flag=True, help='Recreate database')
@click.option('--load', is_flag=True, help='Insert data to the database')
def db(db_name, create, drop, recreate, load):
    if drop:
        return drop_database(BASE_URL, db_name)

    if create:
        create_database_or_engine(BASE_URL, db_name, ENGINE_OPTIONS)

    if recreate:
        drop_database(BASE_URL, db_name)
        create_database_or_engine(BASE_URL, db_name, ENGINE_OPTIONS)

    if load:
        prepare_db()


if __name__ == '__main__':
    cli()
