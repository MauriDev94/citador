from fastapi import FastAPI

from app import __version__
from app.core.health import router as health_router


def create_app() -> FastAPI:
    """Construye una instancia nueva de la aplicación.

    Es una fábrica, no una variable global: cada test obtiene una app
    limpia y la construcción queda abierta a parametrización.
    """
    app = FastAPI(
        title="Citador",
        description="Asistente RAG de documentación técnica con citas obligatorias",
        version=__version__,
    )
    app.include_router(health_router)
    return app
