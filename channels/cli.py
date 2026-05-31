"""AGENTIK CLI — Interface para ejecutar comandos desde terminal."""

import sys
import subprocess


def run_command(command: str) -> str:
    """Execute a shell command and return its output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "ERROR: Command timed out"
    except Exception as e:
        return f"ERROR: {str(e)}"


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage: agentik run \"command\"")
        sys.exit(1)

    if sys.argv[1] == "run":
        command = sys.argv[2]
        output = run_command(command)
        print(output)
    else:
        print(f"Unknown command: {sys.argv[1]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
