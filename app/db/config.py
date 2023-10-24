import os
from peewee import SqliteDatabase

current_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(current_dir, 'report.db')

db = SqliteDatabase(DB_PATH)


