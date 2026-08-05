import pytest
from fastapi.testclient import TestClient

from app.main import create_app

pytestmark = pytest.mark.integration

# Puerto 9 (discard): no hay nadie escuchando, la conexión se rechaza al instante.
UNREACHABLE_DATABASE_URL = "postgresql+asyncpg://nadie:nada@localhost:9/vacia"


def test_should_return_ready_when_database_is_reachable(
    monkeypatch: pytest.MonkeyPatch, test_database_url: str
) -> None:
    monkeypatch.setenv("DATABASE_URL", test_database_url)

    with TestClient(create_app()) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_should_return_503_when_database_is_unreachable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", UNREACHABLE_DATABASE_URL)

    with TestClient(create_app()) as client:
        response = client.get("/health/ready")

    assert response.status_code == 503


def test_should_keep_liveness_ok_when_database_is_unreachable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", UNREACHABLE_DATABASE_URL)

    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
