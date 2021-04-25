import os

import databases
import ormar
import sqlalchemy

DB_CONNECTOR = os.getenv('DB_CONNECTOR')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')

DB_URL = f'{DB_CONNECTOR}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}'

db = databases.Database(DB_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = db


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'users'

    id = ormar.Text(primary_key=True)
    display_name = ormar.Text()
    href = ormar.Text()
    email = ormar.Text()
    country = ormar.Text()
    uri = ormar.Text()
    refresh_token = ormar.Text()
    hashed_password = ormar.Text()


class UserToken(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'user_tokens'

    id = ormar.Integer(primary_key=True, autoincrement=True)
    user = ormar.ForeignKey(User)
    access_token = ormar.Text(nullable=True)


class Track(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'tracks'

    id = ormar.Text(primary_key=True)
    name = ormar.Text()
    href = ormar.Text()
    popularity = ormar.Integer()
    danceability = ormar.Float(nullable=True)
    energy = ormar.Float(nullable=True)
    loudness = ormar.Float(nullable=True)
    speechiness = ormar.Float(nullable=True)
    acousticness = ormar.Float(nullable=True)
    instrumentalness = ormar.Float(nullable=True)
    liveness = ormar.Float(nullable=True)
    valence = ormar.Float(nullable=True)
    tempo = ormar.Float(nullable=True)
    key = ormar.Integer(nullable=True)
    mode = ormar.Integer(nullable=True)
    duration_ms = ormar.Integer(nullable=True)
    time_signature = ormar.Integer(nullable=True)


class Artist(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'artists'

    id = ormar.Text(primary_key=True)
    name = ormar.Text()
    href = ormar.Text()
    popularity = ormar.Integer(nullable=True)


class Genre(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'genres'

    id = ormar.Integer(primary_key=True, autoincrement=True)
    artist = ormar.ForeignKey(Artist)
    genre = ormar.Text()


class TrackArtist(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'tracks_artists'

    id = ormar.Integer(primary_key=True, autoincrement=True)
    artist = ormar.ForeignKey(Artist)
    track = ormar.ForeignKey(Track)


class PlayedTrack(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'played_tracks'

    id = ormar.Integer(primary_key=True, autoincrement=True)
    user = ormar.ForeignKey(User)
    track = ormar.ForeignKey(Track)
    played_at = ormar.DateTime()


if __name__ == '__main__':
    # create the database
    # note that in production you should use migrations
    # note that this is not required if you connect to existing database
    engine = sqlalchemy.create_engine(DB_URL)
    # just to be sure we clear the db before
    metadata.drop_all(engine)
    metadata.create_all(engine)
