import pytest

from src.app import create_app


@pytest.fixture
def app():
    """Create test Flask application"""
    test_app = create_app()
    test_app.config["TESTING"] = True
    return test_app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestAPIEndpoints:
    """Test API endpoint functionality"""

    def test_root_endpoint(self, client):
        """Root endpoint should return welcome message"""
        response = client.get("/")

        assert response.status_code == 200
        assert response.json == {"status": "Welcome"}

    def test_find_country_missing_ip_parameter(self, client):
        """Should return error when IP parameter is missing"""
        response = client.get("/v1/find-country")

        assert response.status_code == 400
        assert response.json == {"error": "IP parameter is missing"}

    def test_find_country_invalid_ip_format(self, client):
        """Should return error for invalid IP format"""
        response = client.get("/v1/find-country?ip=invalid.ip")

        assert response.status_code == 400
        assert "error" in response.json
        assert "Invalid IP address format" in response.json["error"]

    def test_find_country_ip_not_found(self, client):
        """Should return error when IP not found in database"""
        # Use private IP that won't be in test database
        response = client.get("/v1/find-country?ip=192.168.1.1")

        assert response.status_code == 404
        assert "error" in response.json

    def test_rate_limiting_blocks_excess_requests(self, client):
        """Should block requests when rate limit exceeded"""
        # Send requests rapidly to trigger rate limiting
        responses = []
        for _ in range(15):
            response = client.get("/v1/find-country?ip=8.8.8.8")
            responses.append(response.status_code)

        # Should have some 429 (rate limited) responses
        assert 429 in responses, "Rate limiting should trigger with rapid requests"

    def test_stats_endpoint_returns_data(self, client):
        """Stats endpoint should return database information"""
        response = client.get("/v1/stats")

        assert response.status_code == 200
        assert "status" in response.json
        assert "total_records" in response.json
