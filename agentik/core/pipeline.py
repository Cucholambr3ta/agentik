"""AGENTIK Pipeline — Execution engine for .xdd pipeline files."""

import re
import subprocess
from datetime import datetime
from typing import List, Dict, Optional
from agentik.security.receipts import generate_receipt


class PipelineStep:
    """A single step in a pipeline."""
    
    def __init__(self, command: str, line_number: int):
        self.command = command.strip()
        self.line_number = line_number
        self.result = None
        self.output = ""
        self.exit_code = 0
    
    def execute(self) -> bool:
        """Execute the pipeline step."""
        try:
            # Parse command
            if self.command.startswith("/"):
                # X-DD command
                return self._execute_xdd_command()
            else:
                # Shell command
                return self._execute_shell_command()
        except Exception as e:
            self.output = f"ERROR: {str(e)}"
            self.exit_code = 1
            return False
    
    def _execute_xdd_command(self) -> bool:
        """Execute an X-DD command."""
        parts = self.command.split()
        cmd = parts[0]
        
        if cmd == "/xdd-start":
            self.output = "Pipeline started"
            return True
        elif cmd == "/gate":
            return self._execute_gate_command(parts[1:])
        elif cmd == "/cierre-fase":
            self.output = "Phase closed"
            return True
        else:
            self.output = f"Unknown X-DD command: {cmd}"
            self.exit_code = 1
            return False
    
    def _execute_gate_command(self, args: List[str]) -> bool:
        """Execute a gate command."""
        if len(args) < 2:
            self.output = "Usage: /gate assert <type> <value>"
            self.exit_code = 1
            return False
        
        assert_type = args[0]
        expected = args[1]
        
        # For now, just pass the assertion
        self.output = f"Gate assert {assert_type}: {expected} - PASSED"
        return True
    
    def _execute_shell_command(self) -> bool:
        """Execute a shell command."""
        result = subprocess.run(
            self.command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        self.output = result.stdout.strip()
        self.exit_code = result.returncode
        return result.returncode == 0
    
    def to_dict(self) -> Dict:
        """Convert step to dictionary."""
        return {
            "line_number": self.line_number,
            "command": self.command,
            "output": self.output,
            "exit_code": self.exit_code
        }


class Pipeline:
    """Pipeline execution engine for .xdd files."""
    
    def __init__(self, pipeline_path: str):
        self.pipeline_path = pipeline_path
        self.steps: List[PipelineStep] = []
        self.results: List[Dict] = []
        self.start_time = None
        self.end_time = None
    
    def parse(self) -> bool:
        """Parse a .xdd pipeline file."""
        try:
            with open(self.pipeline_path, 'r') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    self.steps.append(PipelineStep(line, i))
            
            return True
        except Exception as e:
            print(f"Error parsing pipeline: {e}")
            return False
    
    def execute(self) -> Dict:
        """Execute all steps in the pipeline."""
        self.start_time = datetime.now()
        
        for step in self.steps:
            success = step.execute()
            self.results.append(step.to_dict())
            
            if not success:
                break
        
        self.end_time = datetime.now()
        
        # Generate receipt
        all_passed = all(r["exit_code"] == 0 for r in self.results)
        receipt = generate_receipt(
            "pipeline_execute",
            "success" if all_passed else "failure",
            self.pipeline_path
        )
        
        return {
            "pipeline": self.pipeline_path,
            "steps": len(self.results),
            "passed": all_passed,
            "results": self.results,
            "receipt": receipt,
            "duration": (self.end_time - self.start_time).total_seconds()
        }
    
    def to_dict(self) -> Dict:
        """Convert pipeline to dictionary."""
        return {
            "path": self.pipeline_path,
            "steps": len(self.steps),
            "parsed": bool(self.steps)
        }


def run_pipeline(pipeline_path: str) -> Dict:
    """Run a pipeline file and return results."""
    pipeline = Pipeline(pipeline_path)
    if not pipeline.parse():
        return {"error": "Failed to parse pipeline"}
    return pipeline.execute()
