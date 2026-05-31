# memoria.md — Flight Recorder del Proyecto

> Bitácora viva del proyecto. **Lectura obligatoria** al inicio de cada sesión.
> Toda sesión termina actualizando este archivo vía `/cierre-fase`.

## Identidad del Proyecto
- **Nombre:** AGENTIK v5.0
- **Dominio:** Agente de desarrollo con X-DD como runtime de validación
- **Stack:** Python 3.8+
- **Fecha de inicio:** 2026-05-31

## Estado Actual
- **Fase X-DD activa:** 0-Foundation
- **Último hito:** Estructura de proyecto creada
- **Próximo paso:** Instalar entorno de desarrollo

## Decisiones Arquitectónicas Clave
- **2026-05-31:** Estructura de paquete Python con módulos: core, mempalace, security, channels
- **2026-05-31:** XDDAdapter como puente entre AGENTIK y pipelines x-dd
- **2026-05-31:** Receipts HMAC-SHA256 para verificación criptográfica de acciones
- **2026-05-31:** CLI como interfaz principal de usuario

## Riesgos Activos
- Sin pip instalado — bloquea `pip install -e ".[dev]"`

---

## Bitácora de Sesiones

### Sesión 01 — 2026-05-31
- **Meta:** Preparar estructura completa del proyecto AGENTIK
- **Hitos:**
  - Estructura de carpetas creada
  - Módulos implementados: cli.py, xdd_adapter.py, receipts.py
  - 7 pipelines .xdd creados para Fase 0
  - Repo git inicializado con rama develop
- **Decisiones:**
  - Usar subprocess para ejecución de comandos en CLI
  - HMAC-SHA256 con secret_key configurable
  - Pipelines TDD antes que código
- **Bloqueos:** pip no disponible
- **Próxima sesión:** Instalar pip + ejecutar tests
