from unittest.mock import MagicMock, patch, AsyncMock
from fastapi.testclient import TestClient
from datetime import datetime, timezone
from app.main import app
from app.api.v1.endpoints import SENSEBOX_API, BOX_IDS

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


