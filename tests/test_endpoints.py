from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.endpoints import get_temperature_sensor_id, BOX_IDS

client = TestClient(app)

# -----------------------------
#  Fixtures
# -----------------------------
@pytest.fixture
def valid_box_id():
    """Returns a valid box ID from OpenSenseMap."""
    return "5eba5fbad46fb8001b799786"

@pytest.fixture
def invalid_box_id():
    """Returns an invalid box ID."""
    return "invalid_box_id_12345"

@pytest.fixture
def mock_temperature_sensor():
    """Returns mock temperature sensor data."""
    return {
        "_id": "5eba5fbad46fb8001b799789",
        "title": "Temperatur",
        "unit": "°C",
        "lastMeasurement": {
            "value": "23.5",
            "createdAt": datetime.now(timezone.utc).isoformat()
        }
    }

@pytest.fixture
def mock_box_data(mock_temperature_sensor):
    """Returns mock box data with temperature sensor."""
    return {
        "_id": "5eba5fbad46fb8001b799786",
        "name": "Test Box",
        "sensors": [mock_temperature_sensor]
    }

@pytest.fixture
def mock_client():
    """Returns a configured mock client for async operations."""
    mock_async_client = AsyncMock(spec=httpx.AsyncClient)
    mock_response = AsyncMock()
    mock_response.raise_for_status = MagicMock()
    mock_async_client.get.return_value = mock_response
    return mock_async_client

# -----------------------------
#  Integration Tests with OpenSenseMap API
# -----------------------------
@pytest.mark.asyncio
async def test_get_temperature_sensor_id_integration():
    """Integration test: Should fetch real temperature sensor ID from OpenSenseMap."""
    async with httpx.AsyncClient() as async_client:
        for box_id in BOX_IDS:
            sensor_id = await get_temperature_sensor_id(async_client, box_id)
            # Either we get a valid sensor ID or None if no temperature sensor exists
            if sensor_id:
                assert isinstance(sensor_id, str)
                assert len(sensor_id) > 0
            else:
                assert sensor_id is None

@pytest.mark.asyncio
async def test_temperature_endpoint_integration():
    """Integration test: Should fetch real temperature data from OpenSenseMap."""
    response = client.get("/api/v1/temperature")
    assert response.status_code in [200, 503]
    
    data = response.json()
    if response.status_code == 200:
        assert "average_temperature" in data
        assert "unit" in data
        assert data["unit"] == "°C"
        assert "measurements_count" in data
        assert "timestamp" in data
        
        # Validate temperature range (realistic values)
        assert -50 <= data["average_temperature"] <= 60
        assert data["measurements_count"] > 0
    else:
        assert "error" in data
        assert data["error"] == "No recent temperature data available."

# -----------------------------
#  Unit Tests with Mocked Responses
# -----------------------------
@pytest.mark.asyncio
async def test_get_temperature_sensor_id_mocked(mock_client, mock_box_data):
    """Unit test: Should correctly extract temperature sensor ID from mocked response."""
    async def mock_get(*_a, **_k):
        response = AsyncMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = mock_box_data
        return response
    mock_client.get = mock_get
    result = await get_temperature_sensor_id(mock_client, mock_box_data["_id"])
    assert result == mock_box_data["sensors"][0]["_id"]

@pytest.mark.asyncio
async def test_get_temperature_sensor_id_no_sensor(mock_client):
    """Unit test: Should handle case when no temperature sensor exists."""
    async def mock_get(*_a, **_k):
        response = AsyncMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = {"sensors": [{"_id": "other_id", "title": "Humidity"}]}
        return response
    mock_client.get = mock_get
    result = await get_temperature_sensor_id(mock_client, "box_id")
    assert result is None

@pytest.mark.asyncio
async def test_get_temperature_sensor_id_error(mock_client):
    """Unit test: Should handle API errors gracefully."""
    async def mock_get(*_a, **_k):
        raise httpx.HTTPError("API Error")
    mock_client.get = mock_get
    result = await get_temperature_sensor_id(mock_client, "box_id")
    assert result is None

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_temperature_endpoint_mocked(mock_async_client_class, mock_box_data):
    """Unit test: Should correctly process temperature data from mocked responses."""
    # Mock responses
    box_response = AsyncMock()
    box_response.raise_for_status = MagicMock()
    box_response.json.return_value = mock_box_data
    temp_response = AsyncMock()
    temp_response.raise_for_status = MagicMock()
    temp_response.json.return_value = [{
        "value": "23.5",
        "createdAt": (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat()
    }]
    # Configure mock client
    mock_client = AsyncMock()
    # Set up the get method to return different responses based on URL
    def side_effect_get(url, *args, **kwargs):
        if url.endswith(mock_box_data["sensors"][0]["_id"]):
            return temp_response
        else:
            return box_response
    
    mock_client.get.side_effect = side_effect_get
    # Configure context manager
    mock_context = AsyncMock()
    mock_context.__aenter__.return_value = mock_client
    mock_async_client_class.return_value = mock_context
    # Mock the endpoint response to simulate a successful API call
    with patch("app.api.v1.endpoints.get_temperature_sensor_id", return_value=mock_box_data["sensors"][0]["_id"]):
        response = client.get("/api/v1/temperature")
        assert response.status_code == 200
        data = response.json()
        assert "average_temperature" in data
        assert data["average_temperature"] == 23.5
        assert data["unit"] == "°C"
        assert data["measurements_count"] > 0
        assert "timestamp" in data

