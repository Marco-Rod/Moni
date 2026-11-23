# Roadmap

Cada fase se desglosa en issues pequeños. Marcar al cerrar.

- [ ] **Fase 0: Fundaciones** — repo, CI, reglas de rama, migración inicial, `package-lock.json`, `make check` verde
- [ ] **Fase 1: MVP sin IA** — CRUD de categorías, transacciones, obligaciones y deudas; dashboard mensual
- [ ] **Fase 2: Cálculos** — presupuestos, alertas, ratio de endeudamiento, simulador avalancha/bola de nieve
- [ ] **Fase 3: Asistente básico** — cliente Ollama, resumen financiero calculado, chat
- [ ] **Fase 4: RAG** — carga de documentos, chunking, embeddings, recuperación, set de evaluación
- [ ] **Fase 5: Extras** — importación CSV, recomendaciones proactivas, historial de chat

## Decisiones pendientes
- Autenticación (hoy un solo usuario)

## Decididas
- Frontend: React + Vite + Tailwind + TanStack Query (ADR 0003)
