import os
from typing import Dict, List, Optional, Text, Tuple, Union

from databases import Database

DB_CONNECTOR = os.getenv('DB_CONNECTOR')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')

DB_URL = f'{DB_CONNECTOR}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}'


async def insert_table(
    table: Text,
    columns: Union[List[Text], Text],
    values: Union[List[Dict], Dict]
):
    """
    Inerts new value into the specified table.

    Parameters
    ----------
    table : str
        name of the table
    columns : list of str
        names of the columns to update
    values : list of dict
        list of values to insert
    """
    if not isinstance(columns, list):
        columns = [columns]
    if not isinstance(values, list):
        values = [values]
    async with Database(DB_URL) as database:
        query = f'''INSERT INTO {table} \
            ({', '.join(columns)}) \
            VALUES ({', '.join([f':{column}' for column in columns])})'''
        await database.execute_many(query=query, values=values)


async def update_table(
    table: Text,
    columns: Union[List[Text], Text],
    key: Text,
    values: Union[List[Dict], Dict]
):
    """
    Updates values with key on table.

    Parameters
    ----------
    table : str
        name of the table
    columns : list of str
        names of the columns to update
    key : str
        name of the unique identifier
    values : list of dict
        list of values to insert
    """
    if not isinstance(columns, list):
        columns = [columns]
    if not isinstance(values, list):
        values = [values]
    query = f'''UPDATE {table} \
        SET {', '.join([f'{column}=:{column}' for column in columns])} \
        WHERE {f'{key}=:{key}'}'''
    async with Database(DB_URL) as database:
        await database.execute_many(query=query, values=values)


async def select_table(
    table: Text,
    columns: Union[List[Text], Text],
    whereclauses: Optional[List[Tuple]] = None,
):
    """
    Executes a select query.

    Parameters
    ----------
    table : str
        name of the table
    columns : list of str
        names of the columns to select
    whereclauses: list of tuple
        where clauses conditions

    Returns
    -------
    list of dict
        query result
    """
    async with Database(DB_URL) as database:
        if not isinstance(columns, list):
            columns = [columns]
        query = f'''SELECT {', '.join(columns)} FROM {table}'''
        if whereclauses:
            query = f'''{query} WHERE \
                {', '.join([f'{k}{c}{v}' for (k, c, v) in whereclauses])}'''
        results = await database.fetch_all(
            query=query
        )
        if results:
            results = [*map(dict, results)]
        return results


if __name__ == '__main__':
    import sqlalchemy

    metadata = sqlalchemy.MetaData(DB_URL)

    users = sqlalchemy.Table(
        'users',
        metadata,
        sqlalchemy.Column('id', sqlalchemy.String(), primary_key=True),
        sqlalchemy.Column('display_name', sqlalchemy.String()),
        sqlalchemy.Column('href', sqlalchemy.String()),
        sqlalchemy.Column('email', sqlalchemy.String()),
        sqlalchemy.Column('country', sqlalchemy.String()),
        sqlalchemy.Column('product', sqlalchemy.String()),
        sqlalchemy.Column('type', sqlalchemy.String()),
        sqlalchemy.Column('uri', sqlalchemy.String()),
        sqlalchemy.Column('refresh_token', sqlalchemy.String()),
        sqlalchemy.Column('hashed_password', sqlalchemy.String()),
    )

    tracks = sqlalchemy.Table(
        'tracks',
        metadata,
        sqlalchemy.Column('id', sqlalchemy.String(), primary_key=True),
        sqlalchemy.Column('name', sqlalchemy.String()),
        sqlalchemy.Column('href', sqlalchemy.String()),
        sqlalchemy.Column('popularity', sqlalchemy.Integer()),
        sqlalchemy.Column('danceability', sqlalchemy.Float()),
        sqlalchemy.Column('energy', sqlalchemy.Float()),
        sqlalchemy.Column('loudness', sqlalchemy.Float()),
        sqlalchemy.Column('speechiness', sqlalchemy.Float()),
        sqlalchemy.Column('acousticness', sqlalchemy.Float()),
        sqlalchemy.Column('instrumentalness', sqlalchemy.Float()),
        sqlalchemy.Column('liveness', sqlalchemy.Float()),
        sqlalchemy.Column('valence', sqlalchemy.Float()),
        sqlalchemy.Column('tempo', sqlalchemy.Float()),
        sqlalchemy.Column('key', sqlalchemy.Integer()),
        sqlalchemy.Column('mode', sqlalchemy.Integer()),
        sqlalchemy.Column('duration_ms', sqlalchemy.Integer()),
        sqlalchemy.Column('time_signature', sqlalchemy.Integer()),
    )

    artists = sqlalchemy.Table(
        'artists',
        metadata,
        sqlalchemy.Column('id', sqlalchemy.String(), primary_key=True),
        sqlalchemy.Column('name', sqlalchemy.String()),
        sqlalchemy.Column('href', sqlalchemy.String()),
        sqlalchemy.Column('popularity', sqlalchemy.Integer()),
        sqlalchemy.Column('genres', sqlalchemy.String()),
    )

    played_tracks = sqlalchemy.Table(
        'played_tracks',
        metadata,
        sqlalchemy.Column(
            'id',
            sqlalchemy.Integer(),
            primary_key=True, autoincrement=True
        ),
        sqlalchemy.Column(
            'user_id',
            sqlalchemy.String(),
            sqlalchemy.ForeignKey('users.id')
        ),
        sqlalchemy.Column(
            'track_id',
            sqlalchemy.String(),
            sqlalchemy.ForeignKey('tracks.id')
        ),
        sqlalchemy.Column(
            'artist_id',
            sqlalchemy.String(),
            sqlalchemy.ForeignKey('artists.id')
        ),
        sqlalchemy.Column(
            'played_at',
            sqlalchemy.DateTime(),
        ),
    )

    user_token = sqlalchemy.Table(
        'user_token',
        metadata,
        sqlalchemy.Column(
            'id',
            sqlalchemy.String(),
            sqlalchemy.ForeignKey('users.id'),
            primary_key=True
        ),
        sqlalchemy.Column(
            'access_token',
            sqlalchemy.String()
        ),
    )

    played_tracks.drop()
    # tracks.drop()
    # artists.drop()
    # user_token.drop()
    # users.drop()

    played_tracks.create()
    # tracks.create()
    # artists.create()
    # user_token.create()
    # users.create()

    print(__file__)
