# Citador — Project Instructions

<!-- harness:base -->
<!-- Este bloque lo mantiene el harness (github.com/MauriDev94/Mauridev-Harness).
     Editarlo acá se pierde en la próxima sincronización: se edita en el repo
     del harness. Lo que va DEBAJO del cierre de este bloque es de este
     proyecto y no se toca nunca. -->

## Antes de dar una tarea por terminada

```
make check
```

No declares nada terminado sin exit code 0.

Si un gate falla por el entorno y no por el código —Docker apagado, base de
datos ausente— dilo explícitamente. **"No pude verificar" es una respuesta
honesta; "los tests pasan" en ese caso no lo es.**

Después, revisa `git status` y `git diff`: mira lo que realmente cambió, no lo
que creías que ibas a cambiar.

## Decisiones de arquitectura

Cuando se tome una decisión que cumpla las **tres** condiciones:

1. **Difícil de revertir** — cambiar de opinión después cuesta de verdad
2. **Sorprendente sin contexto** — un lector futuro se preguntará "¿por qué así?"
3. **Resultado de un trade-off real** — había alternativas genuinas

OFRECE escribir un ADR en `docs/adr/` antes de seguir. Numeración secuencial:
`0001-slug.md`. Registra la decisión **y las alternativas rechazadas** — el
"por qué no" evita que alguien vuelva a proponerlas en seis meses.

No escribas el ADR sin preguntar. No lo omitas por brevedad.

## Calidad

- `mypy strict` está activo. No agregues `# type: ignore` sin un comentario que
  explique por qué.
- Coverage de **rama**. No escribas tests para subir el número: si una rama no
  vale la pena probarla, quizá no vale la pena que exista.
- Un `ignore` de ruff se declara con justificación en el mismo archivo.

<!-- /harness:base -->

## Qué es este proyecto

Citador es un asistente **RAG** de documentación técnica. Responde **sólo desde
las fuentes, con citas obligatorias** — y si el contexto recuperado no alcanza,
la respuesta correcta es **"no lo sé"**.

Eso no es una preferencia de producto: es la razón de existir del sistema. Un
cambio que permita responder sin fuente respaldatoria rompe el proyecto aunque
todos los tests pasen.

## Arquitectura

Clean Architecture + DDD con *feature slices*:

```
app/
├── core/                 config, data, middleware, DI, router, health
└── features/
    ├── documents/        ingesta: registrar → chunk → embed → store
    ├── query/            RAG: retrieve → prompt grounded → responder con citas
    └── evaluation/       harness de evaluación
```

Cada feature: `domain / application / infrastructure / presentation / di`.

### Regla de oro

El `domain` **no importa** SQLAlchemy, FastAPI, Gemini ni Anthropic.

Los use cases hablan con **puertos** (`LLMProvider`, `EmbeddingProvider`); los
SDKs son *adapters* intercambiables por variable de entorno. Si un caso de uso
importa un SDK directamente, la capa está rota — aunque compile y aunque los
tests pasen.

## Tests

Los tests marcados con `@pytest.mark.integration` necesitan Postgres con
pgvector levantado:

```
make db-up
make migrate-test
```

Sin base de datos, el gate corre sólo los unitarios. Eso está declarado en
`.harness/verify.toml` con `when`, y es a propósito: la cobertura real se mide
en CI, que sí tiene el servicio.

`TEST_DATABASE_URL` se lee del entorno y nunca se hardcodea. `pytest` a secas
no ve tus variables — usa `make test`.
