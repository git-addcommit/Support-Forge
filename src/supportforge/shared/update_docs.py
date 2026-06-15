from pathlib import Path

files = {
    'README.md': """# cipher-fellows UI

A compact Python research interface for model comparison, safe tools, and model evaluation.
This folder contains the Gradio web app, a desktop alternative, and supporting utilities for multi-provider experiments.

## Included files

- `app.py` — Gradio web interface for chat, research guidance, tools, and SpecLab comparisons.
- `desktop_app.py` — Desktop alternative built with PySimpleGUI.
- `timer.py` — Tracks session usage, latency, and model metrics.
- `tools.py` — Safe helper tools for calculator, search, and sandboxed file reading.
- `models.json` — Supported model registry used by the UI.
- `requirements.txt` — Python dependencies.
- `tests/` — Unit tests for timer and tool modules.
- `.env.example` — Template for API keys and provider settings.

## Quick start

```powershell
cd C:\cf\cfui
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` with any available provider keys, then run:

```powershell
python app.py
```

Open `http://localhost:7860` in your browser.

## Main features

- Multi-provider model chat using Ollama, Groq, Anthropic Claude, Gemini, and NVIDIA NIM.
- Research guide assistant for prompt design and planning.
- Safe helper tools: calculator, mocked web search, and sandboxed file reader.
- SpecLab workflow for comparing model responses on scenario-driven tasks.
- Session metrics and per-model usage tracking.

## Notes

- `cipher-fellows/` is a separate workspace project and is not required to run this UI.
- `private-gpt/` is another repository in the workspace and not part of `cfui`.
- `onionpipe-main/` is an unrelated included folder, not used by this project.

## Testing

```powershell
cd C:\cf\cfui
pytest tests/ -v
```
""",
    'COPILOT_INSTRUCTIONS.md': """# CFUI Development Notes

This file summarizes the current development focus for `cfui`.

## Goals

- Keep the UI concise and functional.
- Remove emoji-heavy language from user-facing documentation.
- Use `models.json` to populate model selectors dynamically.
- Ensure sessions and metrics are tracked correctly in `timer.py`.

## Key files

- `app.py` — Main application entry point.
- `desktop_app.py` — Local desktop UI.
- `timer.py` — Usage tracking and metrics.
- `tools.py` — Safe tool implementations.
- `models.json` — Model configuration.
- `tests/test_timer.py` — Timer unit tests.
- `tests/test_tools.py` — Tool unit tests.

## Current tasks

1. Verify `app.py` loads the model list from `models.json`.
2. Confirm `timer.py` records model latency and request counts.
3. Keep `tools.py` outputs deterministic and safe.
4. Update documentation for clarity and consistency.

## Notes

- Add `HELP.md` as a short, practical user guide.
- Keep this file focused on feature and implementation guidance.
""",
    'COPILOT.md': """# cipher-fellows Feature Overview

This document describes the current feature set and roadmap for the `cfui` research interface.

## Purpose

Provide a clean, research-focused interface for multi-model chat, model comparison, and safe helper tools.

## Current features

- **Status**: Environment and model availability checks.
- **Chat**: Interactive conversation with a selected model.
- **Research Guide**: A secondary assistant for prompt design and project questions.
- **Tools**: Calculator, placeholder web search, sandboxed file reader, and document preview.
- **SpecLab**: Compare model responses on scenario-based evaluation tasks.

## Supported models

- `ollama/llama2`
- `ollama/mistral`
- `ollama/neural-chat`
- `groq/llama3-70b-8192`
- `groq/mixtral-8x7b-32768`
- `nim/meta-llama3-8b-instruct`
- `nim/meta-llama3-70b-instruct`
- `nim/mistral-7b-instruct`
- `nim/mixtral-8x7b`
- `anthropic/claude-opus`
- `anthropic/claude-3-5-sonnet-20241022`
- `gemini/gemini-2.0-flash`

## Roadmap

- Validate current Gradio UI flow and dropdown defaults.
- Add result saving for SpecLab and tools outputs.
- Keep documentation concise and easy to follow.

## Run instructions

```powershell
cd C:\cf\cfui
python app.py
```

Or for the desktop app:

```powershell
python desktop_app.py
```
""",
    'START_HERE.txt': """cipher-fellows UI — ready to use

This folder contains the `cfui` application, including a Gradio web app and a desktop UI.

Setup:
  1. cd C:\cf\cfui
  2. python -m venv .venv
  3. .\\.venv\\Scripts\\Activate.ps1
  4. pip install -r requirements.txt
  5. copy .env.example .env
  6. edit .env with any API keys you want to use

Run:
  python app.py
  python desktop_app.py

What is included:
  - Web UI with chat, research guide, tools, and SpecLab
  - Desktop UI alternative
  - Safe runtime tools and session metrics
  - Model registry in models.json

Notes:
  - `cipher-fellows/` is a separate research project.
  - `private-gpt/` is a separate repository in the workspace.
  - `onionpipe-main/` is an unrelated existing folder.
""",
    'HELP.md': """# HELP

Basic setup and usage notes for `cfui`.

## Setup

1. Open a terminal in `C:\cf\cfui`.
2. Create a virtual environment:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Copy the sample environment file:

```powershell
copy .env.example .env
```

5. Edit `.env` to add any provider API keys you require.

## Run the web UI

```powershell
python app.py
```

Open `http://localhost:7860`.

## Run the desktop UI

```powershell
python desktop_app.py
```

## Main UI tabs

- **System Status**: environment checks and model availability.
- **Chat**: conversation with a selected model.
- **Research Guide**: prompt design and project advice.
- **Tools**: calculator, search helper, sandboxed file reader, document preview.
- **SpecLab**: scenario comparison across model responses.

## Common checks

- If the model dropdown is empty, confirm `models.json` exists and is valid.
- If the web UI does not start, ensure dependencies are installed in the active virtual environment.
- If Ollama models are selected, verify `ollama serve` is running.

## Tests

```powershell
pytest tests/ -v
```

## Notes

- `private-gpt/` is not part of this application.
- `onionpipe-main/` is an unrelated folder in the workspace.
"""
}

for name, content in files.items():
    Path(name).write_text(content, encoding='utf-8')
print('Updated', ', '.join(files.keys()))
