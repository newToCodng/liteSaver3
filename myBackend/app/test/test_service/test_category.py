import pytest
import asyncpg
from unittest.mock import patch, AsyncMock
from app.services.categoryService import create_category, get_categories_service
from app.core.exceptions import DatabaseError, CategoryAlreadyExists
from app.models.categoryModel import CategoryIn

# Example valid category data
test_category = CategoryIn(
    name="Test Category",
    category_type="expense"
)


@pytest.mark.asyncio
async def test_create_category_success():
    """Test successful category creation."""
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchval.return_value = 1  # Simulate returning a category ID

        category_id = await create_category(1, test_category)
        assert category_id == 1  # Check if the returned category ID is correct
        mock_conn.fetchval.assert_called_once()  # Ensure fetchval was called once


@pytest.mark.asyncio
async def test_create_category_already_exists():
    """Test category creation raises CategoryAlreadyExists when duplicate."""
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchval.side_effect = asyncpg.UniqueViolationError("Unique violation")

        with pytest.raises(CategoryAlreadyExists):
            await create_category(1, test_category)  # Expecting a CategoryAlreadyExists exception


@pytest.mark.asyncio
async def test_create_category_database_error():
    """Test category creation raises DatabaseError on database failure."""
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchval.side_effect = asyncpg.PostgresError("Database error")

        with pytest.raises(DatabaseError):
            await create_category(1, test_category)  # Expecting a DatabaseError exception


@pytest.mark.asyncio
async def test_get_categories_service_success():
    """Test fetching categories for a user."""
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetch.return_value = [
            {"category_id": 1, "user_id": 1, "name": "Test Category", "category_type": "Expense"},
            {"category_id": 2, "user_id": 1, "name": "Another Category", "category_type": "Income"}
        ]  # Simulate returning a list of categories

        categories = await get_categories_service(1)
        assert len(categories) == 2  # Check if two categories are returned
        assert categories[0]["name"] == "Test Category"  # Check the name of the first category
        mock_conn.fetch.assert_called_once()  # Ensure fetch was called once


@pytest.mark.asyncio
async def test_get_categories_service_database_error():
    """Test fetching categories raises DatabaseError on database failure."""
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetch.side_effect = asyncpg.PostgresError("Database error")

        with pytest.raises(DatabaseError):
            await get_categories_service(1)  # Expecting a DatabaseError exception

