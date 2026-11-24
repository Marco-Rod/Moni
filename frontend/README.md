# Frontend (Moni web)

React 18 + TypeScript + Vite + Tailwind 4 + TanStack Query. Decisión: `docs/decisions/0003-frontend-stack.md`.

```bash
make up                 # http://localhost:5173
```

- Las llamadas van a `/api/*`; Vite las reenvía al backend quitando el prefijo.
- Dinero: la API lo manda como string decimal. Solo formatear con `src/lib/money.ts`.
- Primera vez: ejecuta `npm install` en esta carpeta y **commitea `package-lock.json`** (el CI usa `npm ci`).
