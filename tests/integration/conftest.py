import os

import pytest


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """URL de la base de test, siempre leída del entorno.

    Nunca se hardcodea: en el CI apunta a otro host y este archivo
    no se toca. Si falta, falla fuerte y explica cómo arreglarlo.
    """
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        raise RuntimeError(
            "Falta TEST_DATABASE_URL. Corre los tests con `make test`, "
            "que carga el .env; `pytest` a secas no ve tus variables."
        )
    return url
