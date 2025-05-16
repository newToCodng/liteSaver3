from app.database.connection import db
from app.models.transactionModel import TransactionCreate
from app.database.sql_queries import CREATE_TRANSACTION, UPDATE_ACCOUNT_BALANCE
from app.database.sql_queries import GET_TRANSACTIONS_BY_USER
import asyncpg


async def create_transaction(transaction: TransactionCreate, user_id: int):
    try:
        pool = db.get_pool()
        async with pool.acquire() as conn:
            async with await conn.transaction():
                # Update balance and check ownership and  currency match
                account_id_updated = await conn.fetchval(
                    UPDATE_ACCOUNT_BALANCE,
                    transaction.amount,
                    transaction.account_id,
                    user_id,
                    transaction.currency_id  # Ensure currency matches account's
                )
                if not account_id_updated:
                    raise ValueError("Account not found, access denied, or currency mismatch")

                # Insert transaction
                txn_id = await conn.fetchval(
                    CREATE_TRANSACTION,
                    transaction.account_id,
                    transaction.currency_id,
                    transaction.category_id,
                    transaction.amount,
                    transaction.description,
                )
                return {"transaction_id": txn_id}
    except asyncpg.PostgresError as e:
        raise RuntimeError(f"Transaction failed: {str(e)}")


async def get_transactions(user_id: int) -> list[TransactionCreate]:
    try:
        pool = db.get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(GET_TRANSACTIONS_BY_USER, user_id)
            # Map rows to Transaction models
            transactions = [
                TransactionCreate(
                    account_id=row['account_id'],
                    currency_id=row['currency_id'],
                    category_id=row['category_id'],
                    amount=row['amount'],
                    description=row['description'],
                    created_at=row['created_at']
                )
                for row in rows
            ]
            return transactions
    except asyncpg.PostgresError as e:
        raise RuntimeError(f"Failed to fetch transactions: {str(e)}")
