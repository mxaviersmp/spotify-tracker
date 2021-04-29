import asyncio
import os

from app.api.dependencies.security import get_password_hash
from app.database.db import db
from app.database.schema import User


async def main():
    """Creates first admin user if on fresh db."""
    first_admin_id = os.getenv('FIRST_ADMIN_ID')
    first_admin_email = os.getenv('FIRST_ADMIN_EMAIL')
    first_admin_password = os.getenv('FIRST_ADMIN_PASSWORD')
    async with db:
        admin = await User.objects.get_or_none(id=first_admin_id)
        if not admin or True:
            await User.objects.update_or_create(**{
                'id': 'flycher',
                'email': first_admin_email,
                'hashed_password': get_password_hash(first_admin_password),
                'scopes': 'admin'
            })

if __name__ == '__main__':
    asyncio.run(main())
