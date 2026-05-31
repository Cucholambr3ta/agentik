"""AGENTIK Observabilidad — Logging estructurado y métricas."""

import logging
import json
from datetime import datetime
from typing import Dict, Any


class StructuredFormatter(logging.Formatter):
    """JSON structured log formatter."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        return json.dumps(log_entry)


class MetricsCollector:
    """Simple metrics collector."""
    
    def __init__(self):
        self.metrics: Dict[str, int] = {
            "agentik_tasks_total": 0,
            "agentik_pipelines_total": 0,
            "agentik_receipts_total": 0
        }
    
    def increment(self, metric: str, value: int = 1) -> None:
        """Increment a metric counter."""
        if metric in self.metrics:
            self.metrics[metric] += value
    
    def get_metrics(self) -> Dict[str, int]:
        """Get all metrics."""
        return self.metrics.copy()
    
    def reset(self) -> None:
        """Reset all metrics."""
        for key in self.metrics:
            self.metrics[key] = 0


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Setup structured logging for AGENTIK."""
    logger = logging.getLogger("agentik")
    logger.setLevel(getattr(logging, level.upper()))
    
    handler = logging.StreamHandler()
    handler.setFormatter(StructuredFormatter())
    logger.addHandler(handler)
    
    return logger


# Global metrics instance
metrics = MetricsCollector()
