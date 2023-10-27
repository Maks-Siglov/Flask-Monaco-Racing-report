DB_PATH = 'app/db'
DB_NAME = 'report.db'
ENGINE = 'sqlite'

BASE_URL = f'{ENGINE}:///{DB_PATH}'

TEST_DB_PATH = r'tests/test_db'
TEST_DB_NAME = 'test_db.db'

TEST_BASE_URL = f'{ENGINE}:///{TEST_DB_PATH}'

ENGINE_OPTIONS = {'echo': True}
