import asyncio
import os

from app.api.dependencies.security import get_password_hash
from app.database.db import db
from app.database.schema import User
from app.utils.logger import logger


async def main():
    """Creates first admin user if on fresh db."""
    first_admin_id = os.getenv('FIRST_ADMIN_ID')
    first_admin_email = os.getenv('FIRST_ADMIN_EMAIL')
    first_admin_password = os.getenv('FIRST_ADMIN_PASSWORD')
    async with db:
        admin = await User.objects.get_or_none(id=first_admin_id)
        if not admin:
            logger.info('Creating first admin user.')
            await User.objects.create(**{
                'id': first_admin_id,
                'email': first_admin_email,
                'hashed_password': get_password_hash(first_admin_password),
                'scopes': 'admin'
            })

if __name__ == '__main__':
    asyncio.run(main())
