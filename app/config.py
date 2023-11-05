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


APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')
APP_DEBUG = os.getenv('app_debug')

BASE_URL = f'{ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'

ENGINE_OPTIONS = {'echo': True}
