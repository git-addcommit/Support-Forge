#!/usr/bin/env python3
"""log_run.py — Run a command, log all output with timestamps."""
import subprocess
import sys
import datetime
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python log_run.py <command> [args...]")
    sys.exit(1)

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
log_file = log_dir / f"terminal_{timestamp}.log"

cmd = sys.argv[1:]
print(f"Logging to: {log_file}")
print(f"Running: {' '.join(cmd)}")
print("-" * 60)

with open(log_file, "w") as f:
    f.write(f"# Command: {' '.join(cmd)}\n")
    f.write(f"# Started: {datetime.datetime.now().isoformat()}\n")
    f.write("# " + "-" * 60 + "\n\n")
    f.flush()

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        formatted = f"[{ts}] {line}"
        print(formatted, end="")
        f.write(formatted)
        f.flush()

    process.wait()

    f.write(f"\n# Exit code: {process.returncode}\n")
    f.write(f"# Ended: {datetime.datetime.now().isoformat()}\n")

print(f"\n[exit code {process.returncode}]")
print(f"Log saved to: {log_file}")
sys.exit(process.returncode)
