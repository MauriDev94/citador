from fastapi import APIRouter
from pydantic import BaseModel

from app import __version__

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
    El readiness (`/health/ready`) llega en el chip 0.2.
    """
    return HealthResponse(status="ok", version=__version__)
