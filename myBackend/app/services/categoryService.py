from app.database.connection import db
from app.core.exceptions import DatabaseError, CategoryAlreadyExists
from app.models.categoryModel import CategoryIn
import asyncpg


# define categories by user_id
async def create_category(user_id: int, category: CategoryIn):
    query = """
        INSERT INTO categories (user_id, name, category_type)
        VALUES ($1, $2, $3)
        RETURNING category_id;
    """

    try:
        pool = db.get_pool()
        async with pool.acquire() as conn:
            category_id = await conn.fetchval(query, user_id, category.name, category.category_type)
            return category_id
    except asyncpg.UniqueViolationError as e:
        raise CategoryAlreadyExists(f"Category already exists: {str(e)}")  # attempted duplicate categories
    except asyncpg.PostgresError as e:
        raise DatabaseError(f"Database operation failed: {str(e)}")


# fetch all user-related category rows in a dictionary format
async def get_categories_service(user_id: int):
    query = """
        SELECT category_id, user_id, name, category_type
        FROM categories
        WHERE user_id = $1  
    """
    try:
        pool = db.get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(query, user_id)
            return [dict(row) for row in rows]
    except asyncpg.PostgresError as e:
        raise DatabaseError(f"Database operation failed: {str(e)}")
