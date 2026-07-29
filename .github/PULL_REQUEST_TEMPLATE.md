## 📌 Issue relacionado

Closes #<!-- número del issue -->

## 🧠 Resumen

_Qué hace este PR, en 2-3 líneas._

## 🧩 Feature / módulo afectado

- [ ] `documents` (ingesta)
- [ ] `query` (retrieval + generación)
- [ ] `evaluation` (harness)
- [ ] `core` (config, DB, middleware, DI)
- [ ] Infra / CI (Dockerfile, docker-compose, Makefile, `.github/`)

## 📂 Archivos modificados

| Archivo | Cambio |
|---------|--------|
| `path/to/file` | _Qué cambió y por qué_ |

## ✅ Checklist

**Calidad**
- [ ] Lint + format pasan: `ruff check . && ruff format --check .`
- [ ] Type checking pasa: `mypy app`
- [ ] Tests pasan: `pytest -q` → N passed, 0 failed
- [ ] Coverage no baja del gate (`fail_under` en `pyproject.toml`)

**Arquitectura**
- [ ] Sin lógica de negocio en routers (presentación delgada)
- [ ] DIP: sin imports de SQLAlchemy, `google-genai` ni `anthropic` en `domain/` ni `application/`
- [ ] Los use cases hablan con los puertos (`LLMProvider` / `EmbeddingProvider` / `Retriever`), nunca con el SDK
- [ ] Sin migraciones huérfanas: `alembic check` *(desde el chip 0.2)*

**Seguridad** 🔐
- [ ] Sin credenciales, API keys ni tokens en el código o en el historial
- [ ] `.env` NO versionado; `.env.example` solo con placeholders (`changeme`)
- [ ] Variables nuevas documentadas en `.env.example` y leídas desde `Settings`

**Convenciones**
- [ ] Conventional commits (en español)
- [ ] Un solo label `type:*`

## 🧪 Cómo probar

```bash
make check
```

## 📝 Notas técnicas

<!-- Opcional — gotchas, decisiones de diseño no obvias, trade-offs asumidos -->
