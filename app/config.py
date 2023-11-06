

import os

from dotenv import load_dotenv

ENV = os.getenv('ENV', default='LOCAL')

if ENV == 'TEST':
    load_dotenv('.env.test')
else:
    load_dotenv('.env')


DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_HOST = os.getenv('DB_HOST')

ENGINE = os.getenv('ENGINE')

POSTGRESS_DB = os.getenv('POSTGRESS_DB')

APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')
APP_DEBUG = os.getenv('APP_DEBUG', 0)

if ENGINE == 'postgresql+psycopg2':
    BASE_URL = f'{ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
else:
    BASE_URL = ''

ECHO_OPTION = os.getenv('ECHO_OPTION')
ENGINE_OPTIONS = {'echo': int(ECHO_OPTION)}

FOLDER_DATA = r'app/bl/data'
TEMPLATE_FOLDER = 'site/templates'
