# 0001. Stack base

- Fecha: 2026-11-23
- Estado: aceptada

## Contexto
Proyecto personal, datos sensibles, desarrollo mayormente por agentes, ejecución local.

## Decisión
FastAPI + SQLAlchemy 2 + Alembic; PostgreSQL con pgvector (una sola BD para datos y embeddings); Ollama local; Docker Compose. Embeddings con `bge-m3` (1024 dim).

## Consecuencias
- Sin servicio extra de vector DB.
- Cambiar de modelo de embeddings implica migrar la dimensión y re-indexar.
- Hardware: un modelo 7B requiere ~8 GB de RAM libres.
