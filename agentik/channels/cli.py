"""AGENTIK CLI — Interface para ejecutar comandos desde terminal."""

import sys
import subprocess
import json
from datetime import datetime
from agentik.core.history import history


def run_command(command: str) -> tuple[str, int]:
    """Execute a shell command and return its output and exit code."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "ERROR: Command timed out", 1
    except Exception as e:
        return f"ERROR: {str(e)}", 1


def store_in_mempalace(key: str, value: str, wing: str = "Conversations") -> bool:
    """Store a conversation in MemPalace."""
    try:
        from agentik.mempalace.cli import store
        store(key, value, wing=wing)
        return True
    except Exception:
        return False


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage: agentik run \"command\"")
        sys.exit(1)

    if sys.argv[1] == "run":
        command = sys.argv[2]
        output, exit_code = run_command(command)
        print(output)
        
        # Store in history
        history.add(command, output, exit_code)
        
        # Store in MemPalace
        store_in_mempalace(command, output)
    else:
        print(f"Unknown command: {sys.argv[1]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
