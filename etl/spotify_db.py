from typing import Dict, List, Optional, Text, Union

import sqlalchemy
from databases import Database
from rich import print

DB = 'sqlite:///../example.db'

metadata = sqlalchemy.MetaData(DB)

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
    sqlalchemy.Column('popularity', sqlalchemy.String()),
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
    sqlalchemy.Column('popularity', sqlalchemy.String()),
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


async def insert_table(values: Union[List[Dict], Dict], table: sqlalchemy.Table):
    """
    Inerts new value into the specified table.

    Parameters
    ----------
    values : list of dict
        list of values to insert
    table : sqlalchemy.Table
        sql table
    """
    if not isinstance(values, list):
        values = [values]
    async with Database(DB) as database:
        query = table.insert()
        await database.execute_many(query=query, values=values)


async def update_table(
    table: Text, columns: List[Text], key: Text, values: Union[List[Dict], Dict]
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
    if not isinstance(values, list):
        values = [values]
    query = f'''UPDATE {table} \
        SET {', '.join([f'{column}=:{column}' for column in columns])} \
        WHERE {f'{key}=:{key}'}'''
    async with Database(DB) as database:
        await database.execute_many(query=query, values=values)


async def select_table(query: Text, values: Optional[Dict] = None):
    """
    Executes a select query.

    Parameters
    ----------
    query : str
        select query
    values : dict, optional
        values to fill, by default None

    Returns
    -------
    list of dict
        query result
    """
    async with Database(DB) as database:
        results = await database.fetch_all(
            query=query,
            values=values
        )
        if results:
            results = [*map(dict, results)]
        return results


if __name__ == '__main__':
    # users.drop()
    # tracks.drop()
    # artists.drop()
    # played_tracks.drop()
    # user_token.drop()

    # users.create()
    # tracks.create()
    # artists.create()
    # played_tracks.create()
    # user_token.create()

    print(__file__)
