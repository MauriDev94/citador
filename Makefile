.PHONY: help install db-up db-down migrate migrate-test migrate-check lint format typecheck test test-cov check run docker-build docker-run

# Carga .env si existe, para tener PORT y demás variables
-include .env
export

PORT ?= 8000
PY := .venv/Scripts/python.exe

help:  ## Muestra los comandos disponibles
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

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
	$(PY) -m ruff check .

format:  ## Formatea el código con ruff
	$(PY) -m ruff format .

typecheck:  ## Verifica tipos con mypy
	$(PY) -m mypy app

test:  ## Corre los tests
	$(PY) -m pytest

test-cov:  ## Corre los tests midiendo cobertura
	$(PY) -m pytest --cov=app --cov-report=term-missing

check: lint typecheck test  ## Puerta de calidad completa (lo mismo que corre el CI)

run:  ## Levanta la API en modo desarrollo
	$(PY) -m uvicorn app.main:create_app --factory --reload --port $(PORT)

docker-build:  ## Construye la imagen
	docker build -t citador:local .

docker-run:  ## Levanta el contenedor
	docker run --rm -p $(PORT):8000 --name citador citador:local