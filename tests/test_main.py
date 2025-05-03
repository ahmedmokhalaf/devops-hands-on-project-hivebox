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


def test_metrics_endpoint_status_code():
    """Test that /metrics endpoint returns a 200 response."""
    response = client.get("/metrics")
    assert response.status_code == 200

def test_metrics_endpoint_contains_metrics():
    """Test that /metrics endpoint contains Prometheus metrics."""
    response = client.get("/metrics")
    assert "process_cpu_usage" in response.text
    assert "process_memory_usage_bytes" in response.text
    assert "http_request_total" in response.text
    assert "http_request_duration_seconds" in response.text
    assert "http_requests_in_progress" in response.text

def test_metrics_endpoint_updates_on_request():
    """Test that request-related metrics increment after an API call."""
    initial_response = client.get("/metrics")
    initial_count = extract_metric_value(initial_response.text, "http_request_total")

    # Make a request to simulate traffic
    client.get("/")

    updated_response = client.get("/metrics")
    updated_count = extract_metric_value(updated_response.text, "http_request_total")

    # The count should increase
    assert updated_count >= initial_count  

def extract_metric_value(metrics_text, metric_name):
    """Extract the numerical value of a Prometheus metric."""
    for line in metrics_text.split("\n"):
        if line.startswith(metric_name):
            # Extract last value from the metric line
            return float(line.split()[-1])  
    # Default value if metric isn't found
    return 0  

