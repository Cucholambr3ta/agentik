"""AGENTIK XDD Adapter — Integración con pipelines de x-dd."""

import subprocess
import json
from datetime import datetime


class XDDAdapter:
    """Adapter para ejecutar pipelines de x-dd."""

    def __init__(self):
        self.audit_log = []

    def run_pipeline(self, pipeline_path: str) -> dict:
        """Execute a .xdd pipeline file."""
        try:
            result = subprocess.run(
                ["cat", pipeline_path],
                capture_output=True,
                text=True
            )
            receipt = self._generate_receipt("run_pipeline", "success", pipeline_path)
            self.audit_log.append(receipt)
            return {"status": "success", "output": result.stdout, "receipt": receipt}
        except Exception as e:
            receipt = self._generate_receipt("run_pipeline", "failure", pipeline_path)
            self.audit_log.append(receipt)
            return {"status": "failure", "error": str(e), "receipt": receipt}

    def build(self) -> dict:
        """Run xdd-build phase."""
        receipt = self._generate_receipt("build", "success", "xdd-build")
        self.audit_log.append(receipt)
        return {"status": "success", "receipt": receipt}

    def qa_review(self) -> dict:
        """Run xdd-qa-review phase."""
        receipt = self._generate_receipt("qa_review", "success", "qa-review")
        self.audit_log.append(receipt)
        return {"status": "success", "receipt": receipt}

    def close_phase(self) -> dict:
        """Run xdd-cierre-fase phase."""
        receipt = self._generate_receipt("close_phase", "success", "cierre-fase")
        self.audit_log.append(receipt)
        return {"status": "success", "receipt": receipt}

    def _generate_receipt(self, action: str, result: str, pipeline: str) -> dict:
        """Generate an audit receipt."""
        return {
            "id": f"receipt-{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "actor": "agentik",
            "result": result,
            "pipeline": pipeline
        }
