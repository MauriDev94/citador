from fastapi.testclient import TestClient

from app.main import create_app


def test_should_return_200_when_health_is_requested() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_should_expose_only_status_and_version_when_health_is_requested() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    payload = response.json()
    assert set(payload) == {"status", "version"}
    assert payload["version"]
