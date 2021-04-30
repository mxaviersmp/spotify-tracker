import os
import re
from importlib.metadata import version

from semantic_version import Version

from . import api, database, spotify, utils

__version__ = str(Version.coerce(version(__package__)))
match = re.match(r'.+\-(\D+)(\d+)', __version__)
if match is not None:
    pre_release_str = match.group(1)
    pre_release_num = match.group(2)
    __version__ = __version__.replace(
        f'{pre_release_str}{pre_release_num}', f'{pre_release_str}.{pre_release_num}'
    )

if os.getenv('APP_LAMBDA'):
    from mangum import Mangum

    from .api.main import app

    handler = Mangum(app)
