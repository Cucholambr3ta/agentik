# CLAUDE.md — Contexto del Proyecto AGENTIK

## Identidad
- **Nombre:** AGENTIK v5.0
- **Propósito:** Agente de desarrollo con X-DD como runtime de validación
- **Stack:** Python 3.8+

## Pipeline X-DD
```
Briefing → Spec → Plan → Build → QA → Retro
```
Cada fase requiere aprobación explícita antes de continuar.

## Comandos Clave
```bash
agentik run "comando"    # Ejecutar comando
xdd gate status          # Estado del pipeline
xdd gate approve <fase>  # Aprobar fase
```

## Estructura
```
agentik/
├── agentik/          # Código fuente
│   ├── core/         # Lógica central
│   ├── mempalace/    # Fork MemPalace
│   ├── security/     # HMAC receipts
│   └── channels/     # CLI, XDD adapter
├── tests/pipelines/  # Pipelines .xdd
├── docs/             # Documentación
└── pyproject.toml
```

## Reglas
1. Trabajar en rama `develop` o `feat/*`
2. Cada tarea → un PR → revisión → merge
3. X-DD valida antes de continuar
4. Nada está completo hasta que X-DD lo diga
