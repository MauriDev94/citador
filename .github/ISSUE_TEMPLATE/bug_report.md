---
name: "🐛 Bug report"
about: Reportar un comportamiento incorrecto en la API o en el pipeline RAG
title: "bug: <descripción breve>"
labels: ["bug"]
assignees: ""
---

## Descripción
<!-- ¿Qué está fallando? Sé concreto. -->

## Feature / módulo afectado
- [ ] `documents` (ingesta)
- [ ] `query` (retrieval + generación)
- [ ] `evaluation` (harness)
- [ ] `core` (config, DB, middleware, DI)
- [ ] Infra (Postgres/pgvector, Docker, compose, CI)

## Pasos para reproducir
1.
2.
3.

## Comportamiento esperado
<!-- ¿Qué debería pasar? -->

## Comportamiento actual
<!-- ¿Qué pasa en realidad? Incluí status code / body, o la respuesta del LLM si aplica. -->

## Capa afectada
- [ ] Domain (entidades / value objects / reglas de negocio)
- [ ] Application (use cases / puertos)
- [ ] Infrastructure (repositorios / adapters de LLM y embeddings / retriever)
- [ ] Presentation (routers HTTP / schemas)
- [ ] Core / Config (middleware / exceptions / DB / DI)

## Contexto técnico
- **Endpoint:** `<METHOD> /ruta`
- **Request ID:** <!-- del middleware de observabilidad -->
- **Proveedores activos:** `LLM_PROVIDER=` / `EMBEDDING_PROVIDER=`
- **Entorno:** local / CI / Render

## Si es un problema de calidad de respuesta (RAG)
<!-- Completá solo si el bug es "respondió mal", no "reventó". -->
- **Pregunta:**
- **Chunks recuperados (top-k y scores):**
- **Respuesta obtenida:**
- **¿Citó fuentes?** sí / no / citó fuentes inexistentes (alucinación)

## Logs relevantes
```
<!-- pegá acá las líneas de log con el request id -->
```

## Criterios de aceptación
- [ ] Test que reproduce el bug (falla antes del fix — TDD)
- [ ] Fix aplicado en la capa correcta
- [ ] `ruff check .` + `ruff format --check .` + `mypy app` en verde
- [ ] `pytest -q` en verde
