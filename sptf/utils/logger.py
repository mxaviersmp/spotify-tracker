import os
import sys

from loguru import logger

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', None)

logger.remove()

format = \
    '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>' \
    ' | ' \
    '<level>{level: <8}</level>' \
    ' | ' \
    '<cyan>{file}</cyan>:<cyan>{line}</cyan> @<cyan>{function}</cyan>' \
    ' - ' \
    '<level>{message}</level>'

logger.add(sys.stdout, format=format, level=LOG_LEVEL)
if LOG_FILE:
    logger.add(LOG_FILE, format=format, level=LOG_LEVEL)
