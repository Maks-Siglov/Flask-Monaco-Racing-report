import os

from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv('db_path')
DB_NAME = os.getenv('db_name')
ENGINE = os.getenv('engine')

BASE_URL = f'{ENGINE}:///{DB_PATH}'

TEST_DB_PATH = os.getenv('test_db_path')
TEST_DB_NAME = os.getenv('test_db_name')

TEST_BASE_URL = f'{ENGINE}:///{TEST_DB_PATH}'

ENGINE_OPTIONS = {'echo': True}
