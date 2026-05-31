# AGENTIK v5.0 — User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Running Commands](#running-commands)
5. [Working with Pipelines](#working-with-pipelines)
6. [Security Features](#security-features)
7. [Monitoring and Metrics](#monitoring-and-metrics)
8. [Troubleshooting](#troubleshooting)

---

## Introduction

AGENTIK v5.0 is a development agent that uses X-DD as a validation runtime. It provides tools for:

- Executing shell commands with history tracking
- Running development pipelines with phase validation
- Maintaining cryptographic audit trails
- Integrating with code analysis tools
- Security scanning and vulnerability detection

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or pipx
- Git

### Install from source

```bash
# Clone the repository
git clone https://github.com/Cucholambr3ta/agentik.git
cd agentik

# Install in development mode
pip install -e ".[dev]"

# Verify installation
agentik --version
```

### Install security tools (optional)

```bash
# Install via pipx (recommended)
pipx install semgrep

# Install gitleaks
curl -sSfL https://raw.githubusercontent.com/gitleaks/gitleaks/master/scripts/install.sh | sh

# Install trivy
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh

# Install nuclei
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

---

## Basic Usage

### Run a simple command

```bash
agentik run "echo 'Hello from AGENTIK'"
```

### Run a Python command

```bash
agentik run "python -c 'print(2 + 2)'"
```

### Run a system command

```bash
agentik run "uname -a"
agentik run "df -h"
agentik run "git status"
```

---

## Running Commands

### Command Execution

When you run a command, AGENTIK:

1. Executes the command in a subprocess
2. Captures stdout and stderr
3. Records the exit code
4. Stores the command in history
5. Generates an audit receipt

### Example

```bash
$ agentik run "ls -la"
total 48
drwxr-xr-x  6 user user 4096 May 31 08:00 .
drwxr-xr-x  3 user user 4096 May 31 07:00 ..
-rw-r--r--  1 user user  105 May 31 08:00 __init__.py
-rw-r--r--  1 user user  131 May 31 08:00 __main__.py
...
```

### Command History

All executed commands are stored in `~/.agentik/history.json`:

```python
from agentik.core.history import history

# View recent commands
recent = history.get_recent(5)

# Search commands
results = history.search("git")

# Get total count
total = history.count()
```

---

## Working with Pipelines

### Pipeline Files

Pipelines are defined in `.xdd` files with the following syntax:

```
/xdd-start
<command>
/gate assert <type> <value>
/cierre-fase
```

### Example Pipeline

Create `tests/pipelines/my_pipeline.xdd`:

```
/xdd-start
echo "Hello from pipeline"
/gate assert salida_contiene "Hello"
/cierre-fase
```

### Execute Pipeline

```python
from agentik.core.pipeline import run_pipeline

result = run_pipeline("tests/pipelines/my_pipeline.xdd")
print(f"Pipeline passed: {result['passed']}")
print(f"Steps executed: {result['steps']}")
```

### Pipeline Steps

| Step | Description |
|------|-------------|
| `/xdd-start` | Initialize pipeline execution |
| `/gate assert` | Validate assertion |
| `/cierre-fase` | Close current phase |

---

## Security Features

### HMAC Receipts

Every action generates a cryptographic receipt:

```python
from agentik.security.receipts import generate_receipt, verify_receipt

# Generate receipt
receipt = generate_receipt("my_action", "success")
print(f"Signature: {receipt['signature']}")

# Verify receipt
is_valid = verify_receipt(receipt)
print(f"Valid: {is_valid}")  # True
```

### Receipt Storage

Receipts are stored locally:

```python
from agentik.security.receipt_storage import receipt_storage

# Create and store
receipt = receipt_storage.create_and_store("deploy", "success")

# Retrieve
retrieved = receipt_storage.retrieve(receipt["id"])

# List recent
receipts = receipt_storage.list_receipts(10)
```

### Security Scanning

Run security audits:

```python
from agentik.core.security_audit import security_auditor

# Run all scanners
results = security_auditor.full_audit()

# Run specific scanner
gitleaks_result = security_auditor.run_gitleaks()
```

---

## Monitoring and Metrics

### View Metrics

```python
from agentik.core.metrics import metrics_exporter

# Get metrics as JSON
print(metrics_exporter.to_json())

# Get metrics in Prometheus format
print(metrics_exporter.to_prometheus())
```

### Available Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `agentik_tasks_total` | counter | Total tasks executed |
| `agentik_pipelines_total` | counter | Total pipelines executed |
| `agentik_receipts_total` | counter | Total receipts generated |
| `agentik_uptime_seconds` | gauge | Uptime in seconds |

### Structured Logging

```python
from agentik.core.observability import setup_logging

logger = setup_logging(level="INFO")
logger.info("Task started")
logger.error("Task failed")
```

Logs are output in JSON format:

```json
{
  "timestamp": "2026-05-31T09:00:00",
  "level": "INFO",
  "logger": "agentik",
  "message": "Task started",
  "module": "my_module",
  "function": "my_function",
  "line": 42
}
```

---

## Troubleshooting

### Command not found

```bash
# Ensure AGENTIK is installed
pip install -e ".[dev]"

# Check PATH
which agentik
```

### Pipeline fails to parse

```bash
# Check .xdd file syntax
cat tests/pipelines/my_pipeline.xdd

# Ensure proper line endings (Unix)
dos2unix tests/pipelines/my_pipeline.xdd
```

### Receipt verification fails

```python
# Ensure receipt hasn't been tampered with
from agentik.security.receipts import verify_receipt

receipt = {...}  # Your receipt
is_valid = verify_receipt(receipt)
if not is_valid:
    print("Receipt has been tampered with!")
```

### GitNexus stale index

```bash
# Re-analyze project
gitnexus analyze

# Check status
gitnexus status
```

### Security tools not found

```bash
# Check if tools are installed
which semgrep gitleaks trivy nuclei

# Install missing tools
pipx install semgrep
```

---

## Getting Help

- **Documentation:** See `docs/` directory
- **API Reference:** See `docs/API.md`
- **Issues:** https://github.com/Cucholambr3ta/agentik/issues
- **X-DD Documentation:** https://github.com/Cucholambr3ta/x-dd
