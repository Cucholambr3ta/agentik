# lecciones.md — Aprendizajes Acumulados

> Lecciones aprendidas del proyecto. Consultado por agentes antes de proponer soluciones.
> Actualizado vía `/cierre-fase` al final de cada fase.

## Formato
```
### [CATEGORÍA] Título breve — YYYY-MM-DD
**Contexto:** Qué estábamos intentando hacer.
**Problema:** Qué falló o sorprendió.
**Causa raíz:** Por qué pasó.
**Lección:** Regla aplicable a futuras decisiones.
**Aplica a:** Ámbito.
```

---

## Lecciones

### [PROCESO] Crear archivos del proyecto en inicialización — 2026-05-31
**Contexto:** Preparación de estructura AGENTIK v5.0.
**Problema:** Se copiaron archivos de otro proyecto en vez de crear versions frescas.
**Causa raíz:** No se siguió el flujo X-DD de creación de artefactos.
**Lección:** Al inicializar proyecto, crear memoria.md, lecciones.md, CLAUDE.md, xdd.profile.yml desde cero con contexto del nuevo proyecto.
**Aplica a:** Inicialización de proyectos.

### [ARQUITECTURA] Pipelines .xdd antes que código — 2026-05-31
**Contexto:** Definición de estructura de validación.
**Problema:** Escribir código primero, tests después.
**Causa raíz:** Falta de disciplina TDD.
**Lección:** Crear archivos .xdd en tests/pipelines/ ANTES de implementar funcionalidad.
**Aplica a:** Toda funcionalidad nueva.
