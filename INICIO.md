# AGENTIK — Instrucciones de inicio para el agente de desarrollo

> **Lee este archivo antes de hacer cualquier cosa.**
> Este proyecto se desarrolla con **X-DD** como motor de desarrollo.

---

## Paso 1 — Activa el orquestador X-DD

Ejecuta el siguiente comando slash para iniciar el pipeline:

```
/xdd
```

X-DD te guiará por las 6 fases del pipeline gated:
`Briefing → Spec → Plan → Build → QA → Retro`

Cada fase requiere aprobación explícita antes de continuar.
**Nada se considera completo hasta que X-DD lo valide.**

---

## Contexto del proyecto

**AGENTIK v5.0** es un agente de desarrollo que usa X-DD como runtime de validación.

El spec completo está en:
```
deepseek_html_20260531_a9ce8d.html
```

Ábrelo y léelo antes de ejecutar `/xdd`. Es el artefacto de la fase **Briefing**.

---

## Qué construir (Phase 0 según el spec)

| Tarea | Módulo | Validación |
|---|---|---|
| 0.1 Fork MemPalace | `agentik/mempalace/` | `xdd gate approve briefing` |
| 0.2 CLI básica | `agentik/channels/cli.py` | tests + gate |
| 0.3 Adapter X-DD | `agentik/channels/xdd_adapter.py` | gate Build |
| 0.4 Receipts HMAC | `agentik/security/receipts.py` | gate QA |
| 0.5 Observabilidad | logging + métricas | gate QA |

---

## Reglas de trabajo

1. **Siempre** trabajar en rama `develop` o `feat/*`. Nunca directo a `main`.
2. Cada tarea → un PR → revisión → merge.
3. Antes de abrir un PR: `xdd gate status` debe mostrar la fase activa en progreso.
4. El release a PyPI solo ocurre cuando **todas las fases** del gate están `APROBADO`.
5. Cuando X-DD publique una nueva versión, llegará un PR automático con las mejoras.
   Revísalo y apruébalo antes de continuar desarrollando.

---

## Comandos clave

```bash
xdd doctor          # verifica el entorno
xdd gate status     # estado del pipeline
xdd gate approve <fase>   # aprobar una fase
xdd update check    # ver si hay actualizaciones de X-DD disponibles
xdd update apply    # aplicar actualizaciones
```

---

*Desarrollado sobre X-DD v0.2.0 · Motor: `pip install x-dd` · Repo: Cucholambr3ta/x-dd*
