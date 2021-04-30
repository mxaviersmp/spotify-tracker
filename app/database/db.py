import os

import databases
import sqlalchemy

DB_CONNECTOR = os.getenv('APP_DB_CONNECTOR')
DB_USERNAME = os.getenv('APP_DB_USERNAME')
DB_PASSWORD = os.getenv('APP_DB_PASSWORD')
DB_HOST = os.getenv('APP_DB_HOST')
DB_PORT = os.getenv('APP_DB_PORT')
DB_DATABASE = os.getenv('APP_DB_DATABASE')

DB_URL = f'{DB_CONNECTOR}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'

db: databases.Database = databases.Database(DB_URL)
metadata: sqlalchemy.MetaData = sqlalchemy.MetaData()
