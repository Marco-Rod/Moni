# Arquitectura

```
[Frontend React/Vite] → [FastAPI api] → [PostgreSQL + pgvector]
                  │
                  └──→ [Ollama] (chat + embeddings)
```

## Capas del backend
- `api/`: routers delgados
- `services/`: lógica de negocio y cálculos financieros (puros y testeables)
- `models/`: SQLAlchemy
- `ai/` (futuro): cliente Ollama, construcción de contexto, RAG, herramientas de solo lectura

## Flujo del asistente (fase 3+)
1. Usuario pregunta.
2. Backend calcula el resumen financiero relevante (servicios).
3. (Fase 4) Recupera fragmentos de conocimiento por similitud (pgvector).
4. Arma el prompt: system estricto + cifras calculadas + fragmentos + pregunta.
5. Ollama responde; se guarda en historial.
