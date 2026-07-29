---
name: "📋 Tarea"
about: Paso de desarrollo, refactor o trabajo técnico (normalmente, un chip del plan)
title: "task: <descripción breve>"
labels: ["task"]
assignees: ""
---

## Descripción
<!-- ¿Qué hay que hacer? Contexto técnico: capas, endpoints, puertos, pipeline RAG. -->

## Feature / módulo afectado
- [ ] `documents` — ingesta: registrar → chunk → embed → store
- [ ] `query` — RAG: retrieve → prompt grounded → generar con citas
- [ ] `evaluation` — harness de evaluación
- [ ] `core` — config, DB, middleware, DI, router
- [ ] Infra / CI — Docker, compose, Makefile, `.github/`

## Capa(s) afectada(s)
- [ ] Domain (entidades / value objects / puertos)
- [ ] Application (use cases)
- [ ] Infrastructure (repositorios / adapters de proveedores)
- [ ] Presentation (routers / schemas)
- [ ] DI (providers)

## Alcance
<!-- Qué entra y qué NO entra en esta tarea. -->

## Criterios de aceptación
- [ ] TDD: tests primero (rojo → verde → refactor)
- [ ] Cambio aislado en la(s) capa(s) correcta(s)
- [ ] DIP: sin imports de SQLAlchemy, `google-genai` ni `anthropic` en `domain/` ni `application/`
- [ ] Los use cases hablan con puertos (`LLMProvider` / `EmbeddingProvider` / `Retriever`), nunca con el SDK
- [ ] Sin credenciales hardcodeadas; `.env` no versionado; `.env.example` solo con placeholders
- [ ] `ruff check .` + `ruff format --check .` + `mypy app` en verde
- [ ] `pytest -q` en verde
- [ ] Sin migraciones huérfanas: `alembic check` *(desde el chip 0.2)*
- [ ] Commit con conventional commits (en español)
