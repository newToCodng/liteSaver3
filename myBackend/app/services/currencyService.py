import asyncpg
from app.database.connection import db
from app.core.exceptions import DatabaseError


# get currency codes
async def get_currency():
    query = """
        SELECT currency_code, currency_id FROM currency;
    """
    try:
        pool = db.get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(query)
            return [dict(row) for row in rows]
    except asyncpg.PostgresError as e:
        raise DatabaseError(f"Database operation failed: {e}")
