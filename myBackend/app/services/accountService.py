import asyncpg
from app.models.accountModel import Account
from app.database.connection import db
from app.core.exceptions import DatabaseError


class AccountAlreadyExists(Exception):
    pass


# service layer for account creation
async def create_account(user_id, account: Account):
    query = """
    INSERT INTO accounts (user_id, currency_id, name, balance, account_type)
    VALUES ($1, $2, $3, $4, $5)
    RETURNING account_id;
    """
    try:
        pool = db.get_pool()
        async with pool.acquire() as conn:
            account_id = await conn.fetchval(query, user_id, account.currency_id, account.name, account.balance, account.account_type)
            return account_id
    except asyncpg.UniqueViolationError as e:
        raise AccountAlreadyExists(f"Account already exists: {str(e)}")


# service layer for providing all accounts related to a user
async def get_accounts(user_id):
    query = """
    SELECT account_id, name, balance FROM accounts
    WHERE user_id = $1
    """
    try:
        pool = db.get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(query, user_id)
            return [dict(row) for row in rows]
    except asyncpg.PostgresError as e:
        raise DatabaseError(f"Database operation failed: {str(e)}")


# service layer for providing account type to the frontend
async def get_account_type():
    account_types = ['Cash', 'Bank', 'Credit Card', 'Investment', 'Loan']
    return account_types

