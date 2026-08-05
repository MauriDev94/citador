from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import __version__
from app.core.data.engine import build_engine, database_url_from_env
from app.core.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Ciclo de vida de la aplicación: lo de antes del yield arranca, lo de después apaga.

    El engine nace acá y no al importar el módulo por tres razones:
    necesita un event loop corriendo, su pool debe cerrarse ordenadamente,
    y así los tests pueden apuntar la app a otra base antes de construirla.
    """
    engine = build_engine(database_url_from_env())
    app.state.engine = engine
    try:
        yield
    finally:
        await engine.dispose()


def create_app() -> FastAPI:
    """Construye una instancia nueva de la aplicación.

    Es una fábrica, no una variable global: cada test obtiene una app
    limpia y la construcción queda abierta a parametrización.
    """
    app = FastAPI(
        title="Citador",
        description="Asistente RAG de documentación técnica con citas obligatorias",
        version=__version__,
        lifespan=lifespan,
    )
    app.include_router(health_router)
    return app
