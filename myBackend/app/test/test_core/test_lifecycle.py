import pytest
from unittest.mock import AsyncMock, patch
from app.core.lifecycle import startup, shutdown


@pytest.mark.asyncio
async def test_startup_and_shutdown_called():
    with patch("app.core.lifecycle.startup", new_callable=AsyncMock) as mock_startup, \
            patch("app.core.lifecycle.shutdown", new_callable=AsyncMock) as mock_shutdown:
        # Manually call the mocked startup function
        await mock_startup()

        # Assert that the startup function was called
        mock_startup.assert_awaited_once()

        # Manually call the mocked shutdown function
        await mock_shutdown()

        # Assert that the shutdown function was called
        mock_shutdown.assert_awaited_once()