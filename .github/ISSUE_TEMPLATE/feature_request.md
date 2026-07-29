---
name: "✨ Feature request"
about: Proponer una nueva funcionalidad o mejora
title: "feat: <descripción breve>"
labels: ["enhancement"]
assignees: ""
---

## Problema / necesidad
<!-- ¿Qué problema resuelve? ¿Por qué vale la pena? No describas la solución todavía. -->

## Propuesta
<!-- ¿Cómo lo resolverías? Endpoints, pipeline, comportamiento esperado. -->

## Feature / módulo involucrado
- [ ] `documents` (ingesta)
- [ ] `query` (retrieval + generación)
- [ ] `evaluation` (harness)
- [ ] `core` (config, DB, middleware, DI)
- [ ] Infra / CI

## Capas involucradas
- [ ] Domain (nuevas entidades / value objects / puertos)
- [ ] Application (nuevos use cases)
- [ ] Infrastructure (repositorios / adapters de proveedores)
- [ ] Presentation (routers / schemas)

## Diseño de API (si aplica)
- **Endpoint:** `<METHOD> /ruta`
- **Request / Response:**

## Impacto en el pipeline RAG (si aplica)
<!-- ¿Toca chunking, embeddings, retrieval o el prompt? -->
- [ ] ⚠️ **Requiere re-indexar el corpus** (cambio de modelo/dimensión de embeddings o de chunking)

## Alternativas consideradas
<!-- ¿Qué otras opciones evaluaste y por qué las descartaste? -->

## Criterios de aceptación
- [ ] TDD: tests primero
- [ ] Regla de dependencia respetada (la capa interna no conoce a la externa)
- [ ] DIP: sin imports de SQLAlchemy, `google-genai` ni `anthropic` en `application/` ni `domain/`
- [ ] Sin credenciales hardcodeadas
- [ ] `ruff check .` + `ruff format --check .` + `mypy app` en verde
- [ ] `pytest -q` en verde, coverage sin bajar del gate
