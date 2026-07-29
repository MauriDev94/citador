# Citador

> Asistente **RAG** de documentación técnica que responde **solo desde las fuentes, con citas obligatorias** — o se rechaza a responder si no hay contexto suficiente.

🚧 **En construcción** — Fase 0 (fundamentos).

## El problema

Un LLM no conoce tu documentación y, cuando no sabe, **inventa con total seguridad**. Citador ataca las dos cosas: recupera los fragmentos relevantes de un corpus propio y obliga al modelo a responder **anclado a esas fuentes**, citándolas. Si el contexto no alcanza, la respuesta correcta es "no lo sé".

## Stack

| Capa | Tecnología |
|---|---|
| Runtime | Python 3.13 · FastAPI · uvicorn |
| Persistencia | SQLAlchemy 2.0 async · Alembic · asyncpg |
| Vector store | PostgreSQL + pgvector (HNSW, distancia coseno) |
| LLM | puerto `LLMProvider` → Gemini Flash (default) · Claude Haiku |
| Embeddings | puerto `EmbeddingProvider` → Gemini · FastEmbed (local) |
| Evaluación | harness propio: faithfulness, context/answer relevance |
| Calidad | ruff · mypy · pytest · Makefile · GitHub Actions |
| Deploy | Docker multi-stage → Render + Supabase |

## Arquitectura

Clean Architecture + DDD con *feature slices*:

```
app/
├── core/                 # config, data, middleware, DI, router, health
└── features/
    ├── documents/        # ingesta: registrar → chunk → embed → store
    ├── query/            # RAG: retrieve → prompt grounded → responder con citas
    └── evaluation/       # harness de evaluación
```

Cada feature: `domain / application / infrastructure / presentation / di`.

**Regla de oro:** el `domain` no importa SQLAlchemy, FastAPI, Gemini ni Anthropic. Los use cases hablan con **puertos**; los SDKs son *adapters* intercambiables por variable de entorno.

## Roadmap

- **Fase 0** — fundamentos: scaffold · DB + pgvector · config y DI
- **Fase 1** — ingesta: dominio · chunking · embeddings · persistencia · `POST /documents`
- **Fase 2** — consulta: retriever · prompt grounded · `POST /ask` · streaming SSE
- **Fase 3** — production-grade: observabilidad · guardrails · **eval harness**
- **Fase 4** — CI + deploy (Render + Supabase)

## Desarrollo

_(Se documenta al cerrar el chip 0.1.)_

## Flujo de trabajo

Issue-first: issue (`task`) → `status:approved` → rama `type/descripción` → TDD → PR con `Closes #N` → revisión → merge. Conventional commits en español.
