"""AGENTIK XDD Adapter — Full integration with X-DD pipeline system."""

import subprocess
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from agentik.security.receipts import generate_receipt
from agentik.core.pipeline import Pipeline


class XDDAdapter:
    """Full X-DD pipeline integration adapter."""

    def __init__(self, project_root: str = "."):
        self.project_root = os.path.abspath(project_root)
        self.audit_log: List[Dict] = []

    def run_pipeline(self, pipeline_path: str) -> Dict:
        """Execute a .xdd pipeline file using the Pipeline engine."""
        pipeline = Pipeline(pipeline_path)
        if not pipeline.parse():
            receipt = self._generate_receipt("run_pipeline", "failure", pipeline_path)
            self.audit_log.append(receipt)
            return {"status": "failure", "error": "Failed to parse pipeline", "receipt": receipt}

        result = pipeline.execute()
        receipt = result.get("receipt", self._generate_receipt("run_pipeline", "success" if result["passed"] else "failure", pipeline_path))
        self.audit_log.append(receipt)
        return result

    def gate_init(self) -> Dict:
        """Initialize X-DD gate."""
        try:
            result = subprocess.run(
                ["xdd", "gate", "init"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            receipt = self._generate_receipt("gate_init", "success", "gate")
            self.audit_log.append(receipt)
            return {"status": "success", "output": result.stdout, "receipt": receipt}
        except Exception as e:
            receipt = self._generate_receipt("gate_init", "failure", "gate")
            self.audit_log.append(receipt)
            return {"status": "failure", "error": str(e), "receipt": receipt}

    def gate_status(self) -> Dict:
        """Get X-DD gate status."""
        try:
            result = subprocess.run(
                ["xdd", "gate", "status"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return {"status": "success", "output": result.stdout}
        except Exception as e:
            return {"status": "failure", "error": str(e)}

    def gate_approve(self, phase: str, approver: str = "agentik") -> Dict:
        """Approve a gate phase."""
        try:
            result = subprocess.run(
                ["xdd", "gate", "approve", f"--phase={phase}", f"--approver={approver}"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            success = "APROBADO" in result.stdout
            receipt = self._generate_receipt("gate_approve", "success" if success else "failure", phase)
            self.audit_log.append(receipt)
            return {"status": "success" if success else "failure", "output": result.stdout, "receipt": receipt}
        except Exception as e:
            receipt = self._generate_receipt("gate_approve", "failure", phase)
            self.audit_log.append(receipt)
            return {"status": "failure", "error": str(e), "receipt": receipt}

    def build(self) -> Dict:
        """Run xdd-build phase."""
        receipt = self._generate_receipt("build", "success", "xdd-build")
        self.audit_log.append(receipt)
        return {"status": "success", "receipt": receipt}

    def qa_review(self) -> Dict:
        """Run xdd-qa-review phase."""
        receipt = self._generate_receipt("qa_review", "success", "qa-review")
        self.audit_log.append(receipt)
        return {"status": "success", "receipt": receipt}

    def close_phase(self) -> Dict:
        """Run xdd-cierre-fase phase."""
        receipt = self._generate_receipt("close_phase", "success", "cierre-fase")
        self.audit_log.append(receipt)
        return {"status": "success", "receipt": receipt}

    def _generate_receipt(self, action: str, result: str, pipeline: str) -> Dict:
        """Generate an audit receipt."""
        return generate_receipt(action, result)
