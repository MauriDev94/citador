"""habilita la extension vector

Revision ID: 617a83bad675
Revises:
Create Date: 2026-08-04 20:02:15.373395

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "617a83bad675"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Habilita pgvector en ESTA base de datos.

    La extensión se instala por base, no por servidor: la imagen trae los
    binarios disponibles, pero cada base debe cargarlos por separado.

    Va en una migración y no en un script de arranque del contenedor porque
    en producción (Supabase) no controlamos ese arranque. Así el mismo paso
    versionado corre igual en desarrollo, en test y en producción.
    """
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    """Quita la extensión.

    Sin `CASCADE` a propósito: si alguna columna `vector` la está usando,
    Postgres se niega a borrarla. Revertir no debe destruir datos en silencio.
    """
    op.execute("DROP EXTENSION IF EXISTS vector")
