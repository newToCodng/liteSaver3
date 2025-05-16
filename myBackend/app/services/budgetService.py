import asyncpg
from app.database.connection import db
from app.models.budgetModel import BudgetCreate
from app.core.exceptions import DatabaseError


async def create_budget(user_id: int, budget: BudgetCreate):
    query = """
        INSERT INTO budgets (user_id, category_id, budget_amount, start_date, end_date)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING budget_id;
    """
    try:
        pool = db.get_pool()
        async with pool.acquire() as conn:
            budget_id = await conn.fetchval(
                query,
                user_id,
                budget.category_id,
                budget.budget_amount,
                budget.start_date,
                budget.end_date
            )
            return {"budget_id": budget_id}
    except asyncpg.PostgresError as e:
        raise DatabaseError(f"Failed to create budget: {str(e)}")


async def get_user_budgets(user_id: int):
    query = """
        SELECT budget_id, category_id, budget_amount, current_amount,
               progress_percentage, start_date, end_date, is_active
        FROM budgets
        WHERE user_id = $1
        ORDER BY start_date DESC;
    """
    try:
        pool = db.get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(query, user_id)
            return [dict(row) for row in rows]
    except asyncpg.PostgresError as e:
        raise DatabaseError(f"Failed to retrieve budgets: {str(e)}")
