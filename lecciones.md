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

### [PROCESO] Respetar directorio de trabajo del proyecto — 2026-05-31
**Contexto:** Creación de estructura AGENTIK.
**Problema:** Se crearon archivos en `/home/.../Desarrollos/agentik/` en vez de `/home/.../Desarrollos/personal/agentik/`.
**Causa raíz:** No se verificó el directorio raíz del proyecto antes de crear archivos.
**Lección:** SIEMPRE preguntar o verificar el path correcto del proyecto antes de crear cualquier archivo o estructura.
**Aplica a:** Inicialización y desarrollo de proyectos.

### [PROCESO] No copiar archivos de otros proyectos — 2026-05-31
**Contexto:** Creación de memoria.md, lecciones.md, CLAUDE.md.
**Problema:** Se copiaron archivos de `/home/.../Desarrollos/` en vez de crear versions frescas para AGENTIK.
**Causa raíz:** Se asumió que los archivos existentes eran reutilizables sin verificar contexto.
**Lección:** Al inicializar proyecto nuevo, crear SIEMPRE archivos desde cero con contexto del nuevo proyecto. Nunca copiar de otros proyectos.
**Aplica a:** Inicialización de proyectos.

### [PROCESO] Ejecutar pre-flight checks ANTES de proceder — 2026-05-31
**Contexto:** Inicio de sesión X-DD.
**Problema:** Se saltaron verificaciones: xdd.profile.yml, .xdd/, memoria.md, lecciones.md, xdd-doctor.sh.
**Causa raíz:** Se asumió que el entorno estaba listo sin verificar.
**Lección:** SIEMPRE ejecutar todos los pre-flight checks del Anexo 0 antes de cualquier acción. No proceder si alguno falla.
**Aplica a:** Cada sesión X-DD.

### [PROCESO] Inicializar GitNexus y MemPalace en setup — 2026-05-31
**Contexto:** Configuración del proyecto.
**Problema:** No se inicializaron GitNexus ni MemPalace durante la creación de la estructura.
**Causa raíz:** Se olvidaron del pipeline de inicialización.
**Lección:** Después de crear estructura y archivos, ejecutar `gitnexus analyze` y `mempalace init . --yes && mempalace mine .` como parte del setup completo.
**Aplica a:** Inicialización de proyectos.

### [DEVOPS] No commitear __pycache__ — 2026-05-31
**Contexto:** Primer commit del proyecto.
**Problema:** Se commitearon archivos `__pycache__/` que no deben ir al repositorio.
**Causa raíz:** Falta de .gitignore configurado antes del primer commit.
**Lección:** Crear .gitignore ANTES del primer commit. Incluir `__pycache__/`, `*.pyc`, `.env`, `venv/`, etc.
**Aplica a:** Todo proyecto Python.

### [PROCESO] Seguir flujo X-DD completamente — 2026-05-31
**Contexto:** Inicio de proyecto AGENTIK.
**Problema:** Se crearon archivos y commits sin seguir el pipeline completo: Briefing → Spec → Plan → Build.
**Causa raíz:** Se priorizó la velocidad sobre el proceso.
**Lección:** Seguir el pipeline X-DD en orden. Cada fase requiere aprobación explícita antes de continuar. No saltar fases.
**Aplica a:** Todo proyecto bajo X-DD.

### [ARQUITECTURA] MemPalace fork desde uv local — 2026-05-31
**Contexto:** Fase 0.1 — Fork MemPalace.
**Problema:** No existía repo remoto de MemPalace para clonar.
**Causa raíz:** MemPalace instalado via uv, no como paquete editable.
**Lección:** Copiar desde `/home/.../.local/share/uv/tools/mempalace/lib/python*/site-packages/mempalace/` cuando no hay repo remoto.
**Aplica a:** Fork de dependencias instaladas localmente.

### [TESTING] Tests antes de gate approval — 2026-05-31
**Contexto:** Fase 0 — gate qa approval.
**Problema:** Gate exige QA_REPORT.md con tests ejecutados.
**Causa raíz:** No se crearon tests unitarios al inicio.
**Lección:** Crear tests en `tests/` ANTES de aprobar gate qa. Ejecutar `pytest -v` y documentar resultados.
**Aplica a:** Todas las fases del pipeline.

### [DEVOPS] Artefactos de gate son obligatorios — 2026-05-31
**Contexto:** Aprobación de fases briefing, spec, plan, qa, retro.
**Problema:** Gate rechazaba aprobación por artefactos faltantes (.xdd/*/).
**Causa raíz:** No se crearon directorios y archivos requeridos por el gate.
**Lección:** Crear `.xdd/<fase>/` con los artefactos obligatorios ANTES de ejecutar `xdd-gate.py approve`.
**Aplica a:** Transiciones entre fases del pipeline.

### [ARQUITECTURA] Módulos independientes para integraciones — 2026-05-31
**Contexto:** Phase 2 — Integration (GitNexus, Security Audit).
**Problema:** Integraciones acopladas al core.
**Causa raíz:** Falta de separación de responsabilidades.
**Lección:** Crear módulos independientes (gitnexus.py, security_audit.py) que encapsulen cada integración.
**Aplica a:** Integraciones con herramientas externas.

### [TESTING] Tests de integración vs unitarios — 2026-05-31
**Contexto:** Phase 2 — Testing de módulos nuevos.
**Problema:** Tests de integración dependen de herramientas instaladas.
**Causa raíz:** No se mockearon dependencias externas.
**Lección:** Mantener tests unitarios separados de tests de integración. Usar pytest marks para diferenciar.
**Aplica a:** Tests que dependen de herramientas externas.
