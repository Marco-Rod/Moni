# Finanzas IA

Sistema personal para llevar ingresos, gastos, obligaciones mensuales, deudas e ingresos extra, con un asistente local (Ollama) que explica, analiza y aconseja sobre *tus* números sin enviar datos a terceros.

> Estado: esqueleto inicial. Ver [`docs/roadmap.md`](docs/roadmap.md).

## Stack
FastAPI · SQLAlchemy 2 · Alembic · PostgreSQL 16 + pgvector · Ollama · Docker Compose · Frontend por decidir.

## Arranque rápido
```bash
cp .env.example .env      # cambia POSTGRES_PASSWORD (y DATABASE_URL en consecuencia)
make up                   # db + api + ollama
make migration m="initial schema"   # primera vez: genera la migración inicial
make migrate
make pull-models          # descarga modelos de Ollama
curl localhost:8000/health
```

## Comandos
`make help` lista todo. Antes de abrir un PR: `make check`.

## Para humanos y agentes
Empieza por [`AGENTS.md`](AGENTS.md). El contexto vive en el repo: `docs/` y los issues de GitHub.

## Aviso
No es asesoría financiera profesional.
