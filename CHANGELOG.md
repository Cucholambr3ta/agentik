# Changelog

All notable changes to AGENTIK will be documented in this file.

## [0.1.0] — unreleased

### Added

- **Phase 0: Foundation**
  - MemPalace fork integration (MIT license)
  - Interactive CLI with history persistence
  - X-DD Adapter for pipeline execution
  - Receipts HMAC-SHA256 for audit trail
  - Observability system (structured logging, metrics)

- **Phase 1: Orchestration**
  - Event Bus (async pub/sub with 14 event types)
  - Context Builder (P4-compliant pipeline)
  - Orchestrator for task coordination

- **Phase 2: API + UI**
  - FastAPI REST endpoints (/health, /chat, /events, /tasks, /skills)
  - WebSocket support for real-time updates
  - Pydantic models for request/response validation

- **Phase 3: Codex**
  - AST-based code analysis using tree-sitter
  - Call graph builder
  - Impact analyzer for change assessment

- **Phase 4: Aegis**
  - Security rules engine with AST + regex detection
  - SAST/DAST scanner (semgrep, gitleaks, trivy, nuclei integration)
  - SQL injection, command injection, eval() detection

- **Phase 5: Hermes**
  - Lessons system (failure detection and recording)
  - Skills system (success pattern capture)

- **Phase 6: Plugins**
  - Plugin contract (ABC interface)
  - Plugin registry
  - Auto-discovery system

- **Phase 7: Self-improvement**
  - Self-improvement opportunity detector
  - Patch generator
  - Validator (x-dd integration)

- **Phase 8: Distribution**
  - GitHub Actions release workflow (PyPI)
  - Auto-update checker (PyPI + GitHub)
  - Package builder (wheel + sdist)

### Fixed

- X-DD Adapter now executes real commands (build/qa_review/close_phase)
- Context Builder properly queries MemPalace via Searcher
- Security rules use AST analysis for SQL/command injection detection

### Security

- HMAC-SHA256 receipts for all actions
- AST-based vulnerability detection
- Integration with semgrep, gitleaks, trivy, nuclei

### Testing

- 64 tests covering all modules
- Real logic tests for HMAC, event bus, context pipeline order
- AST-based security detection tests
