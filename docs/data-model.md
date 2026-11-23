# Modelo de datos

Fuente de verdad: `backend/app/models/`. Este documento resume la intención.

| Tabla | Propósito |
|---|---|
| users | Usuario y moneda base |
| categories | Categorías de ingreso/gasto por usuario |
| transactions | Ingresos y gastos (`nature`: fixed/variable/extra) |
| recurring_obligations | Pagos mensuales (luz, agua, internet…) con día de vencimiento |
| debts | Deudas con banco/financiera/persona: saldo, tasa, pago mínimo |
| debt_payments | Abonos a deudas |
| budgets | Límite mensual por categoría (`month` = día 1) |
| knowledge_documents / knowledge_chunks | Conocimiento para RAG (embeddings `vector(1024)`) |

## Convenciones
- PK UUID; `created_at` / `updated_at` con zona horaria
- Dinero `NUMERIC(14,2)`; tasas `NUMERIC(7,4)` en porcentaje anual
- Enums guardados como texto con CHECK (no enums nativos de Postgres) para facilitar migraciones
- `user_id` en toda tabla de datos del usuario; `knowledge_documents.user_id` NULL = global
