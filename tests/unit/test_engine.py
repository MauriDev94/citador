import pytest

from app.core.data.engine import database_url_from_env


def test_should_raise_when_database_url_is_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Sin DATABASE_URL la app no arranca: nunca hay una base por defecto.

    Un default silencioso sería una credencial hardcodeada con otro nombre.
    """
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        database_url_from_env()
