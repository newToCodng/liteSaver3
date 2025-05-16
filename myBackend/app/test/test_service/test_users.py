import pytest
from unittest.mock import patch, AsyncMock
import asyncpg
from app.services.userService import create_user, authenticate_user
from app.models.userModel import UserRegister, UserLogin
from app.core.exceptions import DatabaseError, UserAlreadyExists, InvalidLoginDetails
from app.core.security import hash_password

# Sample user data for testing
test_user_register = UserRegister(
    email="test@example.com",
    first_name="Test",
    last_name="User ",
    password="securepassword",
    phone_number="07900831433",
    dob="1990-01-01"
)

test_user_login = UserLogin(
    email="test@example.com",
    password="securepassword"
)

@pytest.mark.asyncio
async def test_create_user_success():
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchval.return_value = 1  # Simulate returning a user ID

        user_id = await create_user(test_user_register)
        assert user_id == 1
        mock_conn.fetchval.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_already_exists():
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchval.side_effect = asyncpg.UniqueViolationError("Unique violation")

        with pytest.raises(UserAlreadyExists):
            await create_user(test_user_register)


@pytest.mark.asyncio
async def test_create_user_database_error():
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchval.side_effect = asyncpg.PostgresError("Database error")

        with pytest.raises(DatabaseError):
            await create_user(test_user_register)


@pytest.mark.asyncio
async def test_authenticate_user_success():
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchrow.return_value = {
            "user_id": 1,
            "email": "test@example.com",
            "password_hash": hash_password("securepassword")
        }

        result = await authenticate_user(test_user_login)
        assert result["access_token"] is not None
        assert result["token_type"] == "bearer"
        assert result["message"] == "Login successful ✅"


@pytest.mark.asyncio
async def test_authenticate_user_invalid_email():
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchrow.return_value = None  # Simulate no user found

        with pytest.raises(InvalidLoginDetails):
            await authenticate_user(test_user_login)


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password():
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchrow.return_value = {
            "user_id": 1,
            "email": "test@example.com",
            "password_hash": hash_password("wrongpassword")
        }

        with pytest.raises(InvalidLoginDetails):
            await authenticate_user(test_user_login)


@pytest.mark.asyncio
async def test_authenticate_user_database_error():
    with patch('app.database.connection.db.get_pool') as mock_get_pool:
        mock_conn = AsyncMock()
        mock_get_pool.return_value.acquire.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetchrow.side_effect = asyncpg.PostgresError("Database error")

        with pytest.raises(DatabaseError):
            await authenticate_user(test_user_login)
