import os

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def database_url_from_env() -> str:
    """Lee DATABASE_URL del entorno. Falla explícito si falta.

    Nunca hay un valor por defecto: un default con credenciales es una
    credencial hardcodeada con otro nombre.
    """
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "Falta DATABASE_URL. Copia .env.example a .env y complétalo. "
            "La aplicación no arranca contra una base de datos por defecto."
        )
    return url


def build_engine(url: str) -> AsyncEngine:
    """Crea el engine: la fábrica de conexiones y el pool de la aplicación.

    Uno por proceso. No es una conexión: administra la flota.
    `pool_pre_ping` verifica que la conexión prestada siga viva antes de
    entregarla, en vez de que el request del usuario descubra que murió.
    """
    return create_async_engine(url, pool_pre_ping=True)


async def is_database_reachable(engine: AsyncEngine) -> bool:
    """Verifica que la base responda: pool → conexión → protocolo → servidor.

    `SELECT 1` es la consulta más barata que recorre el camino completo
    sin tocar disco ni depender de ninguna tabla.

    Atrapa OSError además de SQLAlchemyError: cuando el fallo ocurre al
    ABRIR la conexión (puerto muerto, DNS, timeout), el error nace en el
    sistema operativo y SQLAlchemy nunca llega a envolverlo. Medido.
    """
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except (SQLAlchemyError, OSError):
        return False
    return True
