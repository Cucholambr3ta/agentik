# AGENTS.md — Directorio de Agentes AGENTIK

> Agentes especializados disponibles para delegación.

## Agentes

### Architect
- **Skill:** skill-backend-architect
- **Dominio:** Arquitectura macro, diseño de sistemas, patrones
- **Cuándo usar:** Diseño inicial, refactorizaciones grandes, decisiones ADR

### Builder
- **Skill:** skill-web-design-architect, skill-clean-code-architect, skill-perf-auditor
- **Dominio:** Implementación de features, UI, código limpio
- **Cuándo usar:** Escritura de código funcional, optimización

### Product-Manager
- **Skill:** skill-product-prioritizer
- **Dominio:** Estrategia, priorización, roadmap
- **Cuándo usar:** Definición de features, priorización de tareas

### QA-Reviewer
- **Skill:** skill-code-reviewer
- **Dominio:** Revisión de código, calidad, estándares
- **Cuándo usar:** Antes de merge, auditorías de código

### SecOps
- **Skill:** skill-shannon-secops
- **Dominio:** Seguridad, amenazas, auditorías
- **Cuándo usar:** Análisis de vulnerabilidades, hardening

### Maintainer
- **Skill:** N/A
- **Dominio:** Deuda técnica, mantenimiento, limpieza
- **Cuándo usar:** Refactoring, eliminación de código muerto

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **agentik** (108 symbols, 110 relationships, 0 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/agentik/context` | Codebase overview, check index freshness |
| `gitnexus://repo/agentik/clusters` | All functional areas |
| `gitnexus://repo/agentik/processes` | All execution flows |
| `gitnexus://repo/agentik/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
