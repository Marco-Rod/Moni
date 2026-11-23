# 0003. Stack de frontend

- Fecha: 2026-11-23
- Estado: aceptada

## Contexto
Los agentes producen mejor código con stacks muy documentados y tipados. El backend ya es una API REST independiente.

## Decisión
React 18 + TypeScript + Vite + Tailwind CSS 4 + TanStack Query. Proyecto separado en `frontend/`, servido en desarrollo por Vite (puerto 5173) con proxy `/api` → backend.

## Reglas derivadas
- La API serializa dinero como **string decimal** ("1234.50"). El frontend no hace aritmética monetaria con `number`; solo formatea (`src/lib/money.ts`). Los cálculos viven en el backend.
- Datos del servidor con TanStack Query; estado local con `useState`. No agregar librerías de estado global sin ADR.
- Estilos solo con utilidades de Tailwind.

## Consecuencias
- Un servicio más en Docker Compose y un job más en CI.
- Se necesita `package-lock.json` versionado (`npm ci` en CI).
- Pendientes: linter ESLint, Vitest y cliente tipado generado desde OpenAPI (issues futuros).
