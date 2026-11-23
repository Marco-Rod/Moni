# AGENTS.md

Guía para cualquier agente (o persona) que trabaje en este repo. Léela completa antes de escribir código. Si algo contradice una conversación previa, **manda este archivo y `docs/`**.

## Qué es el proyecto
App de finanzas personales (ingresos, gastos, obligaciones mensuales, deudas, ingresos extra) con un asistente local basado en Ollama + RAG. Un solo usuario hoy, pero el esquema es multiusuario desde el inicio. Moneda por defecto: MXN. Idioma de UI, docs y prompts del asistente: español.

## Stack
- Backend: Python 3.12, FastAPI, SQLAlchemy 2 (sync por ahora), Alembic, Pydantic v2
- BD: PostgreSQL 16 + pgvector
- IA: Ollama (chat `qwen2.5:7b`, embeddings `bge-m3`, configurables por `.env`)
- Infra: Docker Compose
- Frontend: pendiente (ver `docs/decisions/`)

## Comandos (úsalos, no inventes otros)
| Comando | Qué hace |
|---|---|
| `make up` / `make down` | Levanta / detiene servicios |
| `make test` | pytest con Postgres real |
| `make lint` / `make fmt` | ruff check+format / autoformato |
| `make typecheck` | mypy estricto |
| `make check` | lint + typecheck + test (lo mismo que el CI) |
| `make migration m="..."` | Genera migración Alembic |
| `make migrate` | Aplica migraciones |

## Estructura
```
backend/app/api/      routers FastAPI (delgados: validan y delegan)
backend/app/models/   modelos SQLAlchemy
backend/app/          (futuro) services/, schemas/, ai/
backend/tests/
docs/                 architecture, data-model, roadmap, decisions/ (ADRs), specs/
infra/                scripts de infraestructura
```
Lógica de negocio va en `services/`, no en routers ni modelos.

## Reglas inviolables
1. **Dinero = `Decimal` / `NUMERIC(14,2)`. Nunca `float`.**
2. **Todo dato de usuario lleva `user_id`** y toda consulta filtra por él.
3. **El LLM no calcula.** Python calcula totales, ratios, intereses y proyecciones; el modelo solo recibe cifras ya calculadas e interpreta. Ver `docs/decisions/0002-llm-no-calcula.md`.
4. **Sin text-to-SQL libre.** El asistente solo accede a datos mediante funciones predefinidas de solo lectura.
5. **Privacidad:** no llamar APIs externas con datos financieros. Sin secretos ni datos reales en el repo, logs o fixtures.
6. **Migraciones:** todo cambio de esquema = migración Alembic con `downgrade` funcional. Nunca editar una migración ya mergeada.
7. **No modificar** `.env`, migraciones ya mergeadas, ni reglas de CI/ramas sin autorización explícita en el issue.
8. Si una decisión importante no está documentada, crea un ADR en `docs/decisions/` en el mismo PR.

## Flujo de trabajo
1. Toma un issue (con criterios de aceptación). Si no es claro o es mayor a ~400 líneas, pide dividirlo; no adivines.
2. Si la funcionalidad es no trivial, escribe/actualiza la spec en `docs/specs/` y espera aprobación.
3. Rama desde `main`: `feat/<n>-descripcion`, `fix/<n>-...`, `docs/<n>-...`.
4. Commits convencionales: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
5. Escribe tests junto con el código. Corre `make check`.
6. Abre PR con la plantilla completa, incluida la sección *Notas para quien continúe*.
7. Un agente **distinto** del autor revisa con la checklist de la plantilla. El humano aprueba el merge.
8. Nunca push directo a `main`. Nunca merge propio.

## Definición de terminado
- [ ] Cumple todos los criterios de aceptación del issue
- [ ] `make check` verde (CI verde)
- [ ] Tests cubren el caso feliz y al menos un caso de error
- [ ] Migración incluida y reversible si cambia el esquema
- [ ] Docs/ADR/roadmap actualizados
- [ ] PR revisado por otro agente y aprobado por el humano

## Traspaso entre agentes
Al terminar o detenerte a medias, deja en el PR/issue: qué quedó hecho, qué falta, decisiones tomadas, problemas conocidos y el siguiente paso concreto. Quien continúe debe poder trabajar solo con eso.

## Asistente de IA: reglas del producto
- Responder solo con datos provistos por funciones del backend y fragmentos recuperados del conocimiento.
- Si falta el dato: decirlo, no inventar cifras.
- Citar el concepto del glosario cuando se use.
- Avisar que no es asesoría profesional en temas de deudas grandes o inversión.
- Cada cambio de modelo o prompt se valida con el set de evaluación (`backend/evals/`, pendiente).

> Las reglas detalladas por fase y la documentación por fase se afinarán en `docs/agent-rules.md` (pendiente de revisión).
