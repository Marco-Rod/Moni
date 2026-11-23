# 0002. El LLM no calcula ni consulta SQL libre

- Fecha: 2026-11-23
- Estado: aceptada

## Contexto
Los modelos pequeños fallan en aritmética y alucinan cifras. Text-to-SQL con modelos chicos es frágil e inseguro.

## Decisión
Todo cálculo lo hace Python. El modelo recibe cifras ya calculadas y fragmentos del conocimiento, y solo interpreta/explica. El acceso a datos es mediante funciones predefinidas de solo lectura.

## Consecuencias
- Respuestas más fiables y auditables.
- Cada nueva capacidad del asistente exige primero una función de servicio con tests.
