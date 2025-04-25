from unittest.mock import MagicMock, patch, AsyncMock
from fastapi.testclient import TestClient
import pytest
from datetime import datetime, timezone
from app.api.v1.endpoints import get_version
from app.main import app

client = TestClient(app)

# -----------------------------
# ✅ Test health check endpoint
# -----------------------------
def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# -----------------------------
# ✅ Test version endpoint
# -----------------------------
def test_version_endpoint():
    """Test the version endpoint to ensure it returns a valid version string."""
    response = client.get("/api/v1/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert isinstance(data["version"], str)

# -----------------------------
# ✅ Test temperature endpoint
# -----------------------------
@patch("httpx.AsyncClient")
def test_temperature_endpoint_success(mock_async_client_class):
    """Test the temperature endpoint success case with mocked data."""
    # Create response objects
    box_response = AsyncMock()
    box_response.raise_for_status = MagicMock()
    box_response.json.return_value = {
        "_id": "5eba5fbad46fb8001b799786",
        "name": "Test Box",
        "sensors": [{
            "_id": "temp_sensor_id",
            "title": "Temperatur"
        }]
    }
    
    temp_response = AsyncMock()
    temp_response.raise_for_status = MagicMock()
    temp_response.json.return_value = [{
        "value": "23.5",
        "createdAt": datetime.now(timezone.utc).isoformat()
    }]
    
    # Configure mock client
    mock_client = AsyncMock()
    
    # Set up the get method to return different responses based on URL
    def side_effect_get(url, *args, **kwargs):
        if url.endswith("temp_sensor_id"):
            return temp_response
        else:
            return box_response
    
    mock_client.get.side_effect = side_effect_get
    
    # Configure context manager
    mock_context = AsyncMock()
    mock_context.__aenter__.return_value = mock_client
    mock_async_client_class.return_value = mock_context
    
    # Make the request
    response = client.get("/api/v1/temperature")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "average_temperature" in data
    assert data["average_temperature"] == 23.5
    assert "unit" in data
    assert data["unit"] == "°C"
    assert "measurements_count" in data
    assert "timestamp" in data

@patch("httpx.AsyncClient")
def test_temperature_endpoint_no_data(mock_async_client_class):
    """Test the temperature endpoint when no data is available."""
    # Create response objects
    box_response = AsyncMock()
    box_response.raise_for_status = MagicMock()
    box_response.json.return_value = {
        "_id": "5eba5fbad46fb8001b799786",
        "name": "Test Box",
        "sensors": [{
            "_id": "temp_sensor_id",
            "title": "Temperatur"
        }]
    }
    
    # Empty measurements array to simulate no data
    temp_response = AsyncMock()
    temp_response.raise_for_status = MagicMock()
    temp_response.json.return_value = []
    
    # Configure mock client
    mock_client = AsyncMock()
    
    # Set up the get method to return different responses based on URL
    def side_effect_get(url, *args, **kwargs):
        if url.endswith("temp_sensor_id"):
            return temp_response
        else:
            return box_response
    
    mock_client.get.side_effect = side_effect_get
    
    # Configure context manager
    mock_context = AsyncMock()
    mock_context.__aenter__.return_value = mock_client
    mock_async_client_class.return_value = mock_context
    
    # Make the request
    response = client.get("/api/v1/temperature")
    
    # Assertions
    assert response.status_code == 503
    data = response.json()
    assert "detail" in data
    assert "error" in data["detail"]
    assert data["detail"]["error"] == "No recent temperature data available."
