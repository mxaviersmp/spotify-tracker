from ormar.exceptions import NoMatch

from app.database.schema import PlayedTrack


async def get_played_tracks(query):
    """Gets user from database."""
    try:
        played_tracks = await PlayedTrack.objects.select_related(
            ['track']
        ).all(**query)
        return played_tracks
    except NoMatch:
        return []
