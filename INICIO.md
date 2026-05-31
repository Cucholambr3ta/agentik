# AGENTIK — Instrucciones de inicio para el agente de desarrollo

> **Lee este archivo antes de hacer cualquier cosa.**
> Este proyecto se desarrolla con **X-DD** como motor de desarrollo.

---

## Paso 1 — Activa el orquestador X-DD

```
/anmax
```

Cuando /anmax arranque, dile: **"lee el spec completo en deepseek_html_20260531_288131.html"**

X-DD te guiará por las 6 fases del pipeline gated:
`Briefing → Spec → Plan → Build → QA → Retro`

Cada fase requiere aprobación explícita. **Nada está terminado sin receipt.**

---

## Spec vigente

| Archivo | Estado |
|---|---|
| `deepseek_html_20260531_288131.html` | ✅ **FUENTE DE VERDAD — usar este** |
| `deepseek_html_20260531_a9ce8d.html` | ⚠️ Spec inicial incompleto (solo Fase 0) |

---

## Estado actual del proyecto

| Fase | Estado |
|---|---|
| Fase 0 — Fundación | ✅ Completada (mempalace fork, CLI, x-dd adapter, receipts, observabilidad) |
| Fase 1 — Orquestación | ⏳ Pendiente |
| Fase 2 — API + UI | ⏳ Pendiente |
| Fase 3 — Codex | ⏳ Pendiente |
| Fase 4 — Aegis | ⏳ Pendiente |
| Fase 5 — Hermes | ⏳ Pendiente |
| Fase 6-8 | ⏳ Pendiente |

**Gate X-DD:** todas las fases aprobadas hasta Fase 0. Continuar desde Fase 1.

---

## Lo que falta ANTES de continuar con Fase 1

El proyecto tiene código funcionando pero **no es instalable** todavía.
Completa esto primero (en orden):

1. **`pyproject.toml`** — name=agentik, version=0.1.0, requires-python>=3.11,
   dependencies=[x-dd>=0.2.0 + las que el código usa], entry-point `agentik = "agentik.__main__:main"`
2. **`VERSION`** — contenido: `0.1.0`
3. **`CHANGELOG.md`** — sección `## [0.1.0] — unreleased`
4. **Fix portabilidad** — `agentik/channels/xdd_adapter.py:25` tiene ruta hardcodeada
   `/home/alejandro/Documentos/Desarrollos/scripts/xdd-gate.py`. Reemplazar por
   `subprocess.run(["xdd", "gate", ...])` usando xdd del PATH.
5. **`.github/workflows/tests.yml`** — pytest 3.10/3.11/3.12 + xdd doctor + shield audit

Verifica con:
```bash
pip install -e .
agentik --help
python3 -m pytest tests/ -v
xdd doctor
```

---

## Reglas de trabajo

1. Trabajar en rama `develop` o `feat/*`. Nunca directo a `main`.
2. Cada tarea → un PR → revisión → merge.
3. `xdd gate status` debe mostrar la fase activa antes de abrir un PR.
4. Release a PyPI solo cuando **todas las fases** del gate estén `APROBADO`.
5. NUNCA rutas absolutas del host en el código (`/home/alejandro/...`).
6. Cuando x-dd publique una nueva versión, llegará un PR automático. Revísalo antes de continuar.

---

## Comandos clave

```bash
xdd --version           # debe ser ≥ 0.2.0
xdd doctor              # verifica el entorno
xdd gate status         # estado del pipeline
xdd gate approve <fase> # aprobar una fase
xdd update check        # ver si hay actualizaciones de X-DD
xdd update apply        # aplicar actualizaciones
```

---

*AGENTIK v5.0 · Motor: x-dd 0.2.0 · Spec: deepseek_html_20260531_288131.html*
