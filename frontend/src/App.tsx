import { useQuery } from "@tanstack/react-query";

import { api } from "./lib/api";

export default function App() {
  const health = useQuery({
    queryKey: ["health"],
    queryFn: () => api<{ status: string }>("/health"),
    retry: false,
  });

  return (
    <main className="mx-auto max-w-2xl p-8">
      <h1 className="text-3xl font-bold">Moni</h1>
      <p className="mt-2 text-slate-600">Tus finanzas, con un asistente que vive en tu equipo.</p>

      <p className="mt-6 text-sm">
        API:{" "}
        {health.isLoading && <span>comprobando…</span>}
        {health.isError && <span className="text-red-600">sin conexión</span>}
        {health.data && <span className="text-green-700">{health.data.status}</span>}
      </p>
    </main>
  );
}
