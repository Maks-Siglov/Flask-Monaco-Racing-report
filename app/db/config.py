from sqlalchemy import create_engine


DB_PATH = 'app/db/report.db'

DB_URL = f'sqlite:///{DB_PATH}'

engine = create_engine(DB_URL)
