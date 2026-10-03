import json

import asyncpg

from app.config import DATABASE_URL, POOL_MAX_SIZE, POOL_MIN_SIZE

async def _init(conn):
    await conn.set_type_codec("jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")

async def create_pool() -> asyncpg.Pool:
    return await asyncpg.create_pool(DATABASE_URL, init=_init, min_size=POOL_MIN_SIZE, max_size=POOL_MAX_SIZE)
