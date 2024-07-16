import os
import asyncpg


async def create_db_pool():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return await asyncpg.create_pool(database_url)
