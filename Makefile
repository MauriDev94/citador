.PHONY: help install db-up db-down migrate migrate-test migrate-check lint format typecheck typecheck-fast test test-cov check check-fast run docker-build docker-run

# Carga .env si existe, para tener PORT y demás variables
-include .env
export

PORT ?= 8000
# Windows pone los ejecutables del venv en Scripts/, POSIX en bin/. Fijar sólo
# uno rompe el Makefile en el otro sistema.
PY := $(if $(wildcard .venv/Scripts/python.exe),.venv/Scripts/python.exe,.venv/bin/python)

# Los gates NO se re-declaran acá: viven en .harness/verify.toml, que es lo
# mismo que leen el CI y los hooks de los agentes. Una declaración, tres puertas.
VERIFY := $(PY) .harness/verify.py

# Se parsea con Python y no con grep/awk a propósito: en Windows el shell que
# usa make no resuelve esas herramientas y el target moría con Error 255.
# `-X utf8` hace falta o los acentos salen corruptos en consola.
help:  ## Muestra los comandos disponibles
	@python -X utf8 -c "import re;[print('  %-16s %s'%(m[1],m[2])) for m in re.finditer(r'^([a-zA-Z_-]+):.*?## (.*)$$',open('$(firstword $(MAKEFILE_LIST))',encoding='utf-8').read(),re.M)]"

install:  ## Sincroniza el entorno con el lockfile
	uv sync --frozen

db-up:  ## Levanta las bases de desarrollo y de test y espera a que estén sanas
	docker compose up -d --wait db db-test

db-down:  ## Detiene las bases (el volumen de desarrollo se conserva)
	docker compose down

migrate:  ## Aplica las migraciones a la base de desarrollo
	$(PY) -m alembic upgrade head

migrate-test:  ## Aplica las migraciones a la base de test
	DATABASE_URL="$(TEST_DATABASE_URL)" $(PY) -m alembic upgrade head

migrate-check:  ## Detecta modelos sin migración (requiere modelos: útil desde el chip 1.4)
	$(PY) -m alembic check

lint:  ## Revisa el código con ruff
	$(VERIFY) --only lint

format:  ## Formatea el código con ruff
	$(PY) -m ruff format .
	$(PY) -m ruff check . --fix

typecheck:  ## Verifica tipos con mypy
	$(VERIFY) --only types

typecheck-fast:  ## Tipos con daemon. Atajo de desarrollo, NO es el gate.
	$(PY) -m mypy.dmypy run -- app

test:  ## Corre los tests unitarios (sin base de datos)
	$(VERIFY) --only tests

test-cov:  ## Suite completa con cobertura. Requiere `make db-up`.
	$(VERIFY) --only tests-integration

check:  ## Puerta de calidad completa. Requiere `make db-up`. Lo mismo que el CI.
	$(VERIFY)

check-fast:  ## Sólo lo que no necesita servicios externos.
	$(VERIFY) --when turn

run:  ## Levanta la API en modo desarrollo
	$(PY) -m uvicorn app.main:create_app --factory --reload --port $(PORT)

docker-build:  ## Construye la imagen
	docker build -t citador:local .

docker-run:  ## Levanta el contenedor
	docker run --rm -p $(PORT):8000 --name citador citador:local