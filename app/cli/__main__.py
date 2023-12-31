

import os
import click

from app.bl.report.console_view import build_from_parser
from app.bl.report.prepare import convert_and_store_data
from app.db.session import (
    set_session,
    pop_session,
    close_dbs
)
from app.db.utils import (
    create_database,
    drop_database,
    init_database,
    create_table,
)
from app.config import (
    DB_NAME,
    BASE_URL,
    POSTGRESS_DB,
    FOLDER_DATA
)


@click.group()
def cli() -> None:
    """This click cli group provides two commands first - report which
    represent at console report in desirable order or report about unique
    driver, the second provide interaction with database: create, drop,
    recreate and insert data to db. If you want report console view use report
    command, if you want to interact with database use db command.
    """
    pass


@cli.command()
@click.option('--files', default=FOLDER_DATA, help='Path to the dir with logs')
@click.option('--driver', help='Shows statistic about driver ')
@click.option('--desc', is_flag=True, default=False, help='Descending order')
def report(files: str, driver: str, desc: bool) -> None:
    if not os.path.exists(files):
        raise ValueError(f"Path {files} from --file argument don't exist")
    set_session()
    build_from_parser(files, driver, desc)
    pop_session()
    close_dbs()


@cli.command()
@click.option('--db_name', default=DB_NAME, help='Name of the database')
@click.option('--create', is_flag=True, help='Create database')
@click.option('--drop', is_flag=True, help='Drop database')
@click.option('--recreate', is_flag=True, help='Recreate database')
@click.option('--load', is_flag=True, help='Insert data to the database')
@click.option('--init', is_flag=True, help='Init database')
def db(
    db_name: str,
    create: bool,
    drop: bool,
    recreate: bool,
    load: bool,
    init: bool,
) -> None:
    base_superuser_url = f'{BASE_URL}/{POSTGRESS_DB}'

    if drop:
        return drop_database(base_superuser_url, db_name)

    if create:
        create_database(base_superuser_url, db_name)

    if recreate:
        drop_database(base_superuser_url, db_name)
        create_database(base_superuser_url, db_name)

    if load:
        set_session()
        create_table()
        convert_and_store_data(FOLDER_DATA)
        pop_session()
        close_dbs()

    if init:
        init_database(BASE_URL, DB_NAME)


if __name__ == '__main__':
    cli()
