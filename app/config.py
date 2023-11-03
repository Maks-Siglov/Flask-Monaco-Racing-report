import os

from dotenv import load_dotenv

ENV = os.getenv('ENV', default='LOCAL')

if ENV == 'TEST':
    load_dotenv('.env.test')
else:
    load_dotenv('.env')

DB_PATH = os.getenv('DB_PATH')
DB_NAME = os.getenv('DB_NAME')

ENGINE = os.getenv('ENGINE')

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

DEBUG = os.getenv('DEBUG')

BASE_URL = f'{ENGINE}:///{DB_PATH}'

ENGINE_OPTIONS = {'echo': True}
