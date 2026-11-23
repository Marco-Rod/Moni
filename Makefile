.PHONY: help up down logs build test lint fmt typecheck check migrate migration psql pull-models

help:            ## Lista de comandos
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "%-14s %s\n", $$1, $$2}'

up:              ## Levanta todos los servicios
	docker compose up -d --build

down:            ## Detiene los servicios
	docker compose down

logs:            ## Logs de la API
	docker compose logs -f api

build:           ## Reconstruye imágenes
	docker compose build

test:            ## Corre pytest (con Postgres real)
	docker compose run --rm api pytest

lint:            ## ruff (lint + formato en modo check)
	docker compose run --rm api sh -c "ruff check . && ruff format --check ."

fmt:             ## Formatea el código
	docker compose run --rm api sh -c "ruff check --fix . && ruff format ."

typecheck:       ## mypy
	docker compose run --rm api mypy app

check: lint typecheck test  ## Todo lo que corre el CI

migrate:         ## Aplica migraciones
	docker compose run --rm api alembic upgrade head

migration:       ## Genera migración: make migration m="descripcion"
	docker compose run --rm api alembic revision --autogenerate -m "$(m)"

psql:            ## Consola de Postgres
	docker compose exec db psql -U $${POSTGRES_USER:-finanzas} -d $${POSTGRES_DB:-finanzas}

pull-models:     ## Descarga modelos de Ollama definidos en .env
	@set -a; . ./.env; set +a; \
	docker compose exec ollama ollama pull $$LLM_MODEL && \
	docker compose exec ollama ollama pull $$EMBEDDING_MODEL
