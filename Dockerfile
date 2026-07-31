# ───────────────────────────────────────────────────────────
# Stage 1 — builder: instala dependencias con todas las herramientas
# ───────────────────────────────────────────────────────────
FROM python:3.13-slim AS builder

# uv como binario, desde su imagen oficial: sin pip, sin curl, sin instalador
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# PRIMERO el manifiesto: esta capa se cachea mientras no cambien las deps
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# ───────────────────────────────────────────────────────────
# Stage 2 — runtime: solo lo necesario para ejecutar
# ───────────────────────────────────────────────────────────
FROM python:3.13-slim AS runtime

RUN groupadd --system citador \
    && useradd --system --gid citador --create-home citador

WORKDIR /app

# El entorno ya construido, sin uv ni herramientas de build
COPY --from=builder --chown=citador:citador /app/.venv /app/.venv
# DESPUÉS el código: es lo que más cambia, va en la última capa
COPY --chown=citador:citador app/ /app/app/

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER citador

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status == 200 else 1)"

CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]