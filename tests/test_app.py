import os

os.environ.pop("PROVIDER_BASE_URL", None)

from app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    data = response.get_json()

    assert data["ok"] is True
    assert data["provider_configured"] is False


def test_search_requires_query():
    client = app.test_client()
    response = client.get("/search")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Missing query parameter: query"


def test_search_without_provider_returns_503():
    client = app.test_client()
    response = client.get("/search?query=hulk")

    assert response.status_code == 503
    assert response.get_json()["error"] == "provider_not_configured"
