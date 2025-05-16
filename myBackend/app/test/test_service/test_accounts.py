import pytest
from unittest.mock import patch, AsyncMock
from app.models.accountModel import Account
import asyncpg
from app.services.accountService import create_account, get_accounts, get_account_type, AccountAlreadyExists, DatabaseError

# Sample account data for testing
test_account = Account(
    currency_id=1,
    name="Test Account",
    balance=1000.0,
    account_type="Cash"
)


@pytest.mark.asyncio
async def test_create_account_success():
    """Test successful account creation."""
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchval.return_value = 1  # Simulate returning an account ID

        account_id = await create_account(1, test_account)
        assert account_id == 1  # Check if the returned account ID is correct
        mock_conn.fetchval.assert_called_once()  # Ensure fetchval was called once


@pytest.mark.asyncio
async def test_create_account_already_exists():
    """Test account creation when the account already exists."""
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchval.side_effect = asyncpg.UniqueViolationError("Unique violation error")

        with pytest.raises(AccountAlreadyExists):
            await create_account(1, test_account)  # Expecting an AccountAlreadyExists exception


@pytest.mark.asyncio
async def test_get_accounts_success():
    """Test retrieving accounts for a user."""
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetch.return_value = [  # Simulate returning a list of accounts
            {"account_id": 1, "name": "Test Account", "balance": 1000.0},
            {"account_id": 2, "name": "Savings Account", "balance": 5000.0}
        ]

        accounts = await get_accounts(1)
        assert len(accounts) == 2  # Check if two accounts are returned
        assert accounts[0]["name"] == "Test Account"  # Check the name of the first account
        mock_conn.fetch.assert_called_once()  # Ensure fetch was called once


@pytest.mark.asyncio
async def test_get_accounts_database_error():
    """Test retrieving accounts when a database error occurs."""
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetch.side_effect = asyncpg.PostgresError("Database error")

        with pytest.raises(DatabaseError):
            await get_accounts(1)  # Expecting a DatabaseError exception


@pytest.mark.asyncio
async def test_get_account_type():
    """Test retrieving account types."""
    account_types = await get_account_type()
    expected_types = ['Cash', 'Bank', 'Credit Card', 'Investment', 'Loan']
    assert account_types == expected_types  # Check if the returned account types match the expected list
