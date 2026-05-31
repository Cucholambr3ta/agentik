# AGENTIK v5.0 — API Documentation

## Core Modules

### agentik.core.history

Command history persistence module.

```python
from agentik.core.history import history

# Add command to history
entry = history.add("echo hello", "hello", exit_code=0)

# Get recent commands
recent = history.get_recent(count=10)

# Search history
results = history.search("echo")

# Get total count
total = history.count()

# Clear history
history.clear()
```

**Class: CommandHistory**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `add()` | `command: str, output: str, exit_code: int` | `Dict` | Add command to history |
| `get_recent()` | `count: int = 10` | `List[Dict]` | Get recent commands |
| `search()` | `query: str` | `List[Dict]` | Search command history |
| `count()` | None | `int` | Get total commands |
| `clear()` | None | `None` | Clear all history |

---

### agentik.core.pipeline

Pipeline execution engine for `.xdd` files.

```python
from agentik.core.pipeline import Pipeline, run_pipeline

# Run a pipeline
result = run_pipeline("tests/pipelines/tarea_0.1.xdd")

# Or use the Pipeline class directly
pipeline = Pipeline("tests/pipelines/tarea_0.1.xdd")
pipeline.parse()
result = pipeline.execute()
```

**Class: Pipeline**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `parse()` | None | `bool` | Parse .xdd file |
| `execute()` | None | `Dict` | Execute pipeline steps |
| `to_dict()` | None | `Dict` | Convert to dictionary |

**Class: PipelineStep**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `execute()` | None | `bool` | Execute the step |
| `to_dict()` | None | `Dict` | Convert to dictionary |

---

### agentik.core.metrics

Metrics export endpoint.

```python
from agentik.core.metrics import metrics_exporter

# Get metrics as dictionary
metrics = metrics_exporter.get_metrics()

# Export as JSON
json_output = metrics_exporter.to_json()

# Export in Prometheus format
prometheus_output = metrics_exporter.to_prometheus()

# Print metrics
metrics_exporter.print_metrics()
```

**Class: MetricsExporter**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `get_metrics()` | None | `Dict` | Get all metrics |
| `to_json()` | None | `str` | Export as JSON |
| `to_prometheus()` | None | `str` | Export Prometheus format |
| `print_metrics()` | None | `None` | Print to stdout |

---

### agentik.core.observability

Structured logging and metrics collection.

```python
from agentik.core.observability import setup_logging, metrics

# Setup logging
logger = setup_logging(level="INFO")

# Log messages
logger.info("Task started")
logger.error("Task failed")

# Increment metrics
metrics.increment("agentik_tasks_total")
metrics.increment("agentik_pipelines_total")

# Get metrics
current_metrics = metrics.get_metrics()

# Reset metrics
metrics.reset()
```

**Class: StructuredFormatter**

JSON structured log formatter for consistent logging.

**Class: MetricsCollector**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `increment()` | `metric: str, value: int = 1` | `None` | Increment counter |
| `get_metrics()` | None | `Dict[str, int]` | Get all metrics |
| `reset()` | None | `None` | Reset all counters |

---

## Security Modules

### agentik.security.receipts

HMAC-SHA256 receipt generation and verification.

```python
from agentik.security.receipts import generate_receipt, verify_receipt

# Generate a receipt
receipt = generate_receipt("my_action", "success")

# Verify a receipt
is_valid = verify_receipt(receipt)  # True

# Verify with custom key
is_valid = verify_receipt(receipt, secret_key="custom-key")
```

**Function: generate_receipt()**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `action` | `str` | required | Action performed |
| `result` | `str` | required | Result of action |
| `secret_key` | `str` | `"agentik-default-key"` | HMAC secret key |

**Returns:** `Dict` with keys: `id`, `timestamp`, `action`, `actor`, `result`, `signature`

**Function: verify_receipt()**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `receipt` | `Dict` | required | Receipt to verify |
| `secret_key` | `str` | `"agentik-default-key"` | HMAC secret key |

**Returns:** `bool` — True if receipt is valid

---

### agentik.security.receipt_storage

Local receipt persistence.

```python
from agentik.security.receipt_storage import receipt_storage

# Create and store a receipt
receipt = receipt_storage.create_and_store("my_action", "success")

# Retrieve a receipt
retrieved = receipt_storage.retrieve(receipt["id"])

# List recent receipts
receipts = receipt_storage.list_receipts(count=10)

# Get receipt count
count = receipt_storage.get_receipt_count()
```

**Class: ReceiptStorage**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `store_receipt()` | `receipt: Dict` | `bool` | Store receipt to file |
| `create_and_store()` | `action: str, result: str, secret_key: str` | `Dict` | Create and store receipt |
| `retrieve()` | `receipt_id: str, secret_key: str` | `Optional[Dict]` | Retrieve and verify |
| `list_receipts()` | `count: int = 10` | `List[Dict]` | List recent receipts |
| `get_receipt_count()` | None | `int` | Get total receipts |

---

## Channel Modules

### agentik.channels.cli

CLI interface for command execution.

```python
from agentik.channels.cli import run_command

# Execute a command
output, exit_code = run_command("echo hello")
# output: "hello"
# exit_code: 0
```

**Function: run_command()**

| Parameter | Type | Description |
|-----------|------|-------------|
| `command` | `str` | Shell command to execute |

**Returns:** `tuple[str, int]` — (output, exit_code)

---

### agentik.channels.xdd_adapter

Full X-DD pipeline integration.

```python
from agentik.channels.xdd_adapter import XDDAdapter

adapter = XDDAdapter()

# Run a pipeline
result = adapter.run_pipeline("tests/pipelines/tarea_0.1.xdd")

# Gate operations
adapter.gate_init()
status = adapter.gate_status()
adapter.gate_approve("briefing", "agentik")

# Phase operations
adapter.build()
adapter.qa_review()
adapter.close_phase()
```

**Class: XDDAdapter**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `run_pipeline()` | `pipeline_path: str` | `Dict` | Execute .xdd pipeline |
| `gate_init()` | None | `Dict` | Initialize X-DD gate |
| `gate_status()` | None | `Dict` | Get gate status |
| `gate_approve()` | `phase: str, approver: str` | `Dict` | Approve a phase |
| `build()` | None | `Dict` | Run build phase |
| `qa_review()` | None | `Dict` | Run QA review |
| `close_phase()` | None | `Dict` | Close current phase |

---

## Integration Modules

### agentik.core.gitnexus

GitNexus code analysis integration.

```python
from agentik.core.gitnexus import gitnexus

# Analyze project
result = gitnexus.analyze()

# Query code patterns
result = gitnexus.query("authentication")

# Analyze impact
result = gitnexus.impact("MyClass", direction="upstream")

# Get symbol context
result = gitnexus.context("my_function")

# Get status
result = gitnexus.status()

# List clusters
result = gitnexus.clusters()

# List processes
result = gitnexus.processes()
```

**Class: GitNexusAnalyzer**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `analyze()` | None | `Dict` | Run GitNexus analysis |
| `query()` | `query: str` | `Dict` | Query code patterns |
| `impact()` | `symbol: str, direction: str` | `Dict` | Analyze change impact |
| `context()` | `name: str` | `Dict` | Get symbol context |
| `status()` | None | `Dict` | Get GitNexus status |
| `clusters()` | None | `Dict` | List functional clusters |
| `processes()` | None | `Dict` | List execution flows |

---

### agentik.core.security_audit

Security scanning tools integration.

```python
from agentik.core.security_audit import security_auditor

# Run individual tools
semgrep_result = security_auditor.run_semgrep()
gitleaks_result = security_auditor.run_gitleaks()
trivy_result = security_auditor.run_trivy()
nuclei_result = security_auditor.run_nuclei()

# Run full audit
full_results = security_auditor.full_audit()
```

**Class: SecurityAuditor**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `run_semgrep()` | `pattern: str = "auto"` | `Dict` | Run Semgrep scanner |
| `run_gitleaks()` | None | `Dict` | Run Gitleaks scanner |
| `run_trivy()` | `target: str = "."` | `Dict` | Run Trivy scanner |
| `run_nuclei()` | `target: str = "."` | `Dict` | Run Nuclei scanner |
| `full_audit()` | None | `Dict` | Run all scanners |
