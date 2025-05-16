import pytest
from unittest.mock import patch, AsyncMock
from app.models.transactionModel import TransactionCreate
from app.services.transactionService import create_transaction
from app.database.sql_queries import CREATE_TRANSACTION, UPDATE_ACCOUNT_BALANCE
import asyncpg
from decimal import Decimal

# Sample transaction data for testing
test_transaction = TransactionCreate(
    account_id=1,
    currency_id=1,
    category_id=1,
    amount=Decimal('100.0'),
    description="Test transaction"
)


@pytest.mark.asyncio
async def test_create_transaction_success():
    """Test successful transaction creation."""
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchval.side_effect = [1, 1]  # Simulate returning account_id and transaction_id

        print("Starting transaction creation test...")
        result = await create_transaction(test_transaction, user_id=1)
        print(f"Transaction creation result: {result}")

        assert result == {"transaction_id": 1}  # Check if the returned transaction ID is correct
        print("Asserting SQL query execution...")

        # Print actual calls to fetchval for debugging
        print("Actual calls to fetchval:")
        for call in mock_conn.fetchval.call_args_list:
            print(call)

        # Verify that the correct SQL queries were executed
        mock_conn.fetchval.assert_any_call(
            UPDATE_ACCOUNT_BALANCE.strip(),
            test_transaction.amount,
            test_transaction.account_id,
            1,
            test_transaction.currency_id
        )
        mock_conn.fetchval.assert_any_call(
            CREATE_TRANSACTION,
            test_transaction.account_id,
            test_transaction.currency_id,
            test_transaction.category_id,
            test_transaction.amount,
            test_transaction.description
        )


@pytest.mark.asyncio
async def test_create_transaction_account_not_found():
    """Test transaction creation raises ValueError when account not found."""
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchval.return_value = None  # Simulate


@pytest.mark.asyncio
async def test_create_transaction_database_error():
    """Test transaction creation raises RuntimeError on database failure."""
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchval.side_effect = asyncpg.PostgresError("Database error")
        with pytest.raises(RuntimeError, match="Transaction failed: Database error"):
            await create_transaction(test_transaction, user_id=1)