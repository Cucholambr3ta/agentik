# AGENTIK v5.0

> Agente de desarrollo con X-DD como runtime de validación

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![X-DD](https://img.shields.io/badge/X--DD-0.2.0-green.svg)](https://github.com/Cucholambr3ta/x-dd)

## Overview

AGENTIK v5.0 es un agente de desarrollo que integra X-DD como runtime de validación. Proporciona herramientas para ejecutar comandos, gestionar pipelines de desarrollo, y mantener un registro criptográfico de todas las acciones.

## Features

- **CLI Interactivo** — Ejecuta comandos shell con persistencia de historial
- **Pipeline Engine** — Ejecuta archivos `.xdd` con validación de fases
- **Receipts HMAC** — Registro criptográfico inmutable de acciones
- **GitNexus Integration** — Análisis de código y dependencias
- **Security Audit** — Integración con semgrep, gitleaks, trivy, nuclei
- **Observabilidad** — Logging estructurado y métricas exportables

## Installation

### From PyPI (when published)

```bash
pip install agentik
```

### From repository

```bash
git clone https://github.com/Cucholambr3ta/agentik.git
cd agentik
pip install -e .
agentik --help
```

**Prerequisites:** `pip install x-dd` (x-dd is the validation engine)

For x-dd 0.2.0 (recommended):
```bash
pipx install git+https://github.com/Cucholambr3ta/x-dd.git@develop
```

## Quick Start

### Run a command

```bash
agentik run "ls -la"
agentik run "python --version"
agentik run "git status"
```

### Execute a pipeline

```python
from agentik.core.pipeline import run_pipeline

result = run_pipeline("tests/pipelines/tarea_0.1.xdd")
print(result["passed"])  # True
```

### Generate a receipt

```python
from agentik.security.receipts import generate_receipt, verify_receipt

receipt = generate_receipt("my_action", "success")
print(receipt["signature"])  # HMAC-SHA256 signature

is_valid = verify_receipt(receipt)  # True
```

### Check metrics

```python
from agentik.core.metrics import metrics_exporter

print(metrics_exporter.to_json())
print(metrics_exporter.to_prometheus())
```

## Architecture

```
agentik/
├── agentik/
│   ├── core/               # Core modules
│   │   ├── history.py      # Command history persistence
│   │   ├── pipeline.py     # Pipeline execution engine
│   │   ├── metrics.py      # Metrics export
│   │   ├── gitnexus.py     # GitNexus integration
│   │   └── security_audit.py  # Security tools
│   ├── channels/           # Communication channels
│   │   ├── cli.py          # CLI interface
│   │   └── xdd_adapter.py  # X-DD integration
│   ├── security/           # Security modules
│   │   ├── receipts.py     # HMAC receipts
│   │   └── receipt_storage.py  # Receipt persistence
│   └── mempalace/          # MemPalace fork (MIT)
├── tests/                  # Unit tests
├── docs/                   # Documentation
└── pyproject.toml          # Package configuration
```

## Development

### Run tests

```bash
pytest tests/ -v
```

### Run security audit

```bash
python -c "from agentik.core.security_audit import security_auditor; print(security_auditor.full_audit())"
```

### Check GitNexus status

```bash
gitnexus analyze
gitnexus status
```

## X-DD Integration

AGENTIK integra completamente con X-DD para validación de pipelines:

```bash
# Initialize gate
python scripts/xdd-gate.py init

# Check status
python scripts/xdd-gate.py status

# Approve phase
python scripts/xdd-gate.py approve --phase=briefing --approver=agentik
```

## Configuration

### Environment Variables

```bash
export XDD_GITNEXUS=1  # Enable GitNexus integration
```

### Project Structure

Create `xdd.profile.yml` in project root:

```yaml
profile: internal
project:
  name: MY_PROJECT
  version: "1.0.0"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [X-DD](https://github.com/Cucholambr3ta/x-dd) — Development pipeline framework
- [MemPalace](https://github.com/palace-mem) — Memory system for AI (MIT License)
- [GitNexus](https://github.com/gitnexus) — Code intelligence platform
