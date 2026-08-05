from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel

from app import __version__
from app.core.data.engine import is_database_reachable

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Contrato del endpoint de liveness."""

    status: str
    version: str


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Liveness: informa que el proceso está en pie.

    NO consulta dependencias externas a propósito. Si fallara por culpa de
    la base de datos, el orquestador reiniciaría instancias sanas y
    convertiría una degradación parcial en una caída total.
    El readiness vive en `/health/ready` y ese sí consulta la base.
    """
    return HealthResponse(status="ok", version=__version__)


class ReadinessResponse(BaseModel):
    """Contrato del endpoint de readiness."""

    status: str


@router.get("/health/ready", response_model=ReadinessResponse)
async def readiness(request: Request, response: Response) -> ReadinessResponse:
    """Readiness: informa si la app puede ATENDER tráfico, no si está viva.

    Devuelve 503 —no 500— para que el balanceador la saque de rotación
    sin que el orquestador la reinicie: no está rota, está sin base.
    """
    if await is_database_reachable(request.app.state.engine):
        return ReadinessResponse(status="ready")

    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return ReadinessResponse(status="unavailable")
