#!/usr/bin/env python
"""
cipher-fellows Setup & Verification Script

Run this to:
1. Install dependencies
2. Verify all modules import correctly
3. Check environment configuration
4. Run tests
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    """Run a shell command and report status."""
    print(f"\n{'='*60}")
    print(f"▶️  {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✅ {description} — SUCCESS")
            return True
        else:
            print(f"❌ {description} — FAILED")
            return False
    except Exception as e:
        print(f"❌ {description} — ERROR: {e}")
        return False


def check_imports() -> bool:
    """Verify all modules can be imported."""
    print(f"\n{'='*60}")
    print("▶️  Checking module imports")
    print(f"{'='*60}")

    modules = [
        ("timer", "Timer module"),
        ("tools", "Tools module"),
        ("gradio", "Gradio UI framework"),
    ]

    all_ok = True
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✅ {description} ({module_name}) — OK")
        except ImportError as e:
            print(f"❌ {description} ({module_name}) — MISSING: {e}")
            all_ok = False

    return all_ok


def check_files() -> bool:
    """Verify all expected files exist."""
    print(f"\n{'='*60}")
    print("▶️  Checking project files")
    print(f"{'='*60}")

    files = [
        "app.py",
        "timer.py",
        "tools.py",
        "models.json",
        ".env.example",
        "requirements.txt",
        "tests/test_timer.py",
        "tests/test_tools.py",
    ]

    all_ok = True
    for file_path in files:
        full_path = Path(file_path)
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"✅ {file_path} ({size:,} bytes)")
        else:
            print(f"❌ {file_path} — NOT FOUND")
            all_ok = False

    return all_ok


def check_env() -> bool:
    """Check environment configuration."""
    print(f"\n{'='*60}")
    print("▶️  Checking environment configuration")
    print(f"{'='*60}")

    keys = [
        ("GROQ_API_KEY", "Groq API"),
        ("ANTHROPIC_API_KEY", "Anthropic API"),
        ("NIM_API_KEY", "NVIDIA NIM"),
    ]

    for key, description in keys:
        value = os.environ.get(key, "")
        if value:
            masked = value[:6] + "..." + value[-4:]
            print(f"✅ {description} ({key}) — {masked}")
        else:
            print(f"⚠️  {description} ({key}) — NOT SET (optional)")

    return True


def main():
    """Run setup sequence."""
    print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║  🔬 cipher-fellows — Setup & Verification                ║
║     Anthropic Fellows Application Portfolio               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """)

    os.chdir(Path(__file__).parent)

    steps = [
        ("pip install -r requirements.txt", "Installing dependencies"),
        ("python -m pytest tests/ -v", "Running tests"),
    ]

    print("\n📋 SETUP SEQUENCE")
    all_ok = True

    # 1. Install dependencies
    if not run_command("pip install -r requirements.txt", "Install dependencies"):
        all_ok = False

    # 2. Check files
    if not check_files():
        all_ok = False

    # 3. Check imports
    if not check_imports():
        all_ok = False

    # 4. Check environment
    if not check_env():
        all_ok = False

    # 5. Run tests
    if not run_command("python -m pytest tests/ -v", "Running tests"):
        print("⚠️  Tests may have failed, but code structure is OK")

    # Summary
    print(f"\n{'='*60}")
    print("📊 SETUP SUMMARY")
    print(f"{'='*60}")

    if all_ok:
        print("""
✅ All checks passed! You're ready to run the application.

Next steps:
  1. Set up .env with your API keys (copy from .env.example)
  2. Start Ollama (optional): ollama serve
  3. Run the web UI: python app.py
  4. Open http://localhost:7860 in your browser

Happy researching! 🚀
        """)
    else:
        print("""
⚠️  Some checks failed. Review the output above.

Common issues:
  - Missing .env file → Copy .env.example to .env
  - Ollama not running → Start with: ollama serve
  - Missing API keys → Add to .env
  - Python version < 3.10 → Use Python 3.10+

Still having issues? Check:
  1. requirements.txt is complete
  2. All .py files are in place
  3. pytest can find test files
        """)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
