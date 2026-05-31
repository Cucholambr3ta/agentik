# AGENTIK v5.0 — Developer Guide

## Table of Contents

1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Adding New Features](#adding-new-features)
4. [Writing Tests](#writing-tests)
5. [Code Style](#code-style)
6. [X-DD Integration](#xdd-integration)
7. [Release Process](#release-process)

---

## Development Setup

### Prerequisites

- Python 3.8+
- pip
- Git
- X-DD (optional, for full pipeline validation)

### Clone and setup

```bash
# Clone repository
git clone https://github.com/Cucholambr3ta/agentik.git
cd agentik

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Verify setup

```bash
# Run tests
pytest tests/ -v

# Check code style
flake8 agentik/
black --check agentik/

# Type checking
mypy agentik/
```

---

## Project Structure

```
agentik/
├── agentik/
│   ├── __init__.py           # Package version
│   ├── __main__.py           # CLI entry point
│   ├── core/                 # Core modules
│   │   ├── __init__.py
│   │   ├── history.py        # Command history
│   │   ├── pipeline.py       # Pipeline engine
│   │   ├── metrics.py        # Metrics export
│   │   ├── observability.py  # Logging & metrics
│   │   ├── gitnexus.py       # GitNexus integration
│   │   └── security_audit.py # Security tools
│   ├── channels/             # Communication
│   │   ├── __init__.py
│   │   ├── cli.py            # CLI interface
│   │   └── xdd_adapter.py    # X-DD adapter
│   ├── security/             # Security modules
│   │   ├── __init__.py
│   │   ├── receipts.py       # HMAC receipts
│   │   └── receipt_storage.py # Receipt storage
│   └── mempalace/            # MemPalace fork (MIT)
├── tests/                    # Unit tests
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_security.py
│   └── test_xdd_adapter.py
├── docs/                     # Documentation
│   ├── API.md
│   ├── USER_GUIDE.md
│   └── DEVELOPER_GUIDE.md
├── scripts/                  # Build scripts
├── pyproject.toml            # Package config
├── README.md                 # Project readme
└── LICENSE                   # MIT License
```

---

## Adding New Features

### 1. Create the module

```python
# agentik/core/my_feature.py

"""AGENTIK My Feature — Description of the feature."""

from typing import Dict, List


class MyFeature:
    """My new feature class."""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
    
    def do_something(self, param: str) -> Dict:
        """Do something amazing."""
        return {"status": "success", "param": param}


# Global instance
my_feature = MyFeature()
```

### 2. Add tests

```python
# tests/test_my_feature.py

"""Tests for My Feature module."""

import pytest
from agentik.core.my_feature import my_feature, MyFeature


def test_my_feature_init():
    """Test initializing MyFeature."""
    feature = MyFeature()
    assert feature.config == {}


def test_do_something():
    """Test do_something method."""
    result = my_feature.do_something("test")
    assert result["status"] == "success"
    assert result["param"] == "test"
```

### 3. Update exports

```python
# agentik/core/__init__.py

from .my_feature import my_feature, MyFeature
```

### 4. Update documentation

Add to `docs/API.md`:

```markdown
### agentik.core.my_feature

Description of my feature.

```python
from agentik.core.my_feature import my_feature

result = my_feature.do_something("test")
```

**Class: MyFeature**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `do_something()` | `param: str` | `Dict` | Do something amazing |
```

---

## Writing Tests

### Test Structure

```python
# tests/test_module.py

"""Tests for Module description."""

import pytest
from agentik.module import MyClass


class TestMyClass:
    """Tests for MyClass."""
    
    def test_init(self):
        """Test initialization."""
        obj = MyClass()
        assert obj is not None
    
    def test_method(self):
        """Test method."""
        obj = MyClass()
        result = obj.method("param")
        assert result == expected
    
    def test_error_handling(self):
        """Test error handling."""
        obj = MyClass()
        with pytest.raises(ValueError):
            obj.method(None)
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_cli.py -v

# Run with coverage
pytest tests/ --cov=agentik --cov-report=html

# Run only failing tests
pytest tests/ -v --lf
```

### Test Markers

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    """Test that takes a long time."""
    pass

@pytest.mark.integration
def test_external_service():
    """Test that requires external service."""
    pass

# Run only fast tests
pytest tests/ -m "not slow"

# Run only unit tests
pytest tests/ -m "not integration"
```

---

## Code Style

### Python Style Guide

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions/classes
- Keep functions under 50 lines
- Keep files under 500 lines

### Formatting

```bash
# Format code
black agentik/

# Sort imports
isort agentik/

# Check style
flake8 agentik/

# Type checking
mypy agentik/
```

### Docstring Format

```python
def my_function(param: str, optional: int = None) -> Dict:
    """Short description of the function.

    Longer description if needed.

    Args:
        param: Description of param
        optional: Description of optional

    Returns:
        Dict with keys: status, data

    Raises:
        ValueError: If param is invalid

    Example:
        >>> result = my_function("test")
        >>> print(result["status"])
        "success"
    """
    pass
```

---

## X-DD Integration

### Gate System

AGENTIK uses X-DD's gate system for pipeline validation:

```python
from agentik.channels.xdd_adapter import XDDAdapter

adapter = XDDAdapter()

# Initialize gate
adapter.gate_init()

# Check status
status = adapter.gate_status()

# Approve phase
adapter.gate_approve("briefing", "agentik")
```

### Creating Pipelines

Create `.xdd` files in `tests/pipelines/`:

```
# tests/pipelines/my_feature.xdd

/xdd-start
agentik run "python -c 'from agentik.core.my_feature import my_feature; print(my_feature.do_something(\"test\"))'"
/gate assert salida_contiene "success"
/cierre-fase
```

### Gate Artifacts

Each phase requires specific artifacts:

```
.xdd/
├── briefing/
│   ├── SPEC.md
│   └── FEATURES.md
├── spec/
│   ├── DOMAIN.md
│   └── THREATS.md
├── plan/
│   └── PLAN.md
├── build/
│   └── (code)
├── qa/
│   └── QA_REPORT.md
└── retro/
    └── lecciones.md
```

---

## Release Process

### Version Bumping

Update version in:

1. `pyproject.toml`
2. `agentik/__init__.py`
3. `README.md`

### Create Release

```bash
# Update version
vim pyproject.toml  # Update version
vim agentik/__init__.py  # Update __version__

# Commit changes
git add .
git commit -m "chore: bump version to X.Y.Z"

# Tag release
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# Push
git push origin main --tags
```

### Publish to PyPI

```bash
# Build package
python -m build

# Upload to PyPI
twine upload dist/*

# Verify
pip install agentik==X.Y.Z
```

### Create GitHub Release

1. Go to GitHub Releases
2. Click "Draft a new release"
3. Select tag
4. Add release notes
5. Publish

---

## Contributing

### Workflow

1. Fork repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes
4. Write tests
5. Run tests: `pytest tests/ -v`
6. Commit: `git commit -m "feat: add my feature"`
7. Push: `git push origin feature/my-feature`
8. Create Pull Request

### Commit Messages

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Maintenance

### Pull Request Checklist

- [ ] Tests pass
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Reviewed by at least one maintainer

---

## Getting Help

- **Issues:** https://github.com/Cucholambr3ta/agentik/issues
- **Discussions:** https://github.com/Cucholambr3ta/agentik/discussions
- **X-DD Docs:** https://github.com/Cucholambr3ta/x-dd
