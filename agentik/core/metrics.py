"""AGENTIK Metrics — Export metrics endpoint."""

import json
from datetime import datetime
from typing import Dict
from agentik.core.observability import metrics
from agentik.core.history import history
from agentik.security.receipt_storage import receipt_storage


class MetricsExporter:
    """Export metrics in various formats."""
    
    def __init__(self):
        self.start_time = datetime.now()
    
    def get_metrics(self) -> Dict:
        """Get all metrics."""
        return {
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "agentik_tasks_total": metrics.metrics.get("agentik_tasks_total", 0),
            "agentik_pipelines_total": metrics.metrics.get("agentik_pipelines_total", 0),
            "agentik_receipts_total": metrics.metrics.get("agentik_receipts_total", 0),
            "agentik_history_count": history.count(),
            "agentik_receipt_files_count": receipt_storage.get_receipt_count()
        }
    
    def to_json(self) -> str:
        """Export metrics as JSON."""
        return json.dumps(self.get_metrics(), indent=2)
    
    def to_prometheus(self) -> str:
        """Export metrics in Prometheus format."""
        m = self.get_metrics()
        lines = [
            f"# HELP agentik_tasks_total Total tasks executed",
            f"# TYPE agentik_tasks_total counter",
            f"agentik_tasks_total {m['agentik_tasks_total']}",
            f"# HELP agentik_pipelines_total Total pipelines executed",
            f"# TYPE agentik_pipelines_total counter",
            f"agentik_pipelines_total {m['agentik_pipelines_total']}",
            f"# HELP agentik_receipts_total Total receipts generated",
            f"# TYPE agentik_receipts_total counter",
            f"agentik_receipts_total {m['agentik_receipts_total']}",
            f"# HELP agentik_uptime_seconds Uptime in seconds",
            f"# TYPE agentik_uptime_seconds gauge",
            f"agentik_uptime_seconds {m['uptime_seconds']:.2f}"
        ]
        return "\n".join(lines)
    
    def print_metrics(self):
        """Print metrics to stdout."""
        print(self.to_json())


# Global metrics exporter instance
metrics_exporter = MetricsExporter()
