# HELP

Basic setup and usage notes for `cfui`.

## Setup

1. Open a terminal in `C:\cf\cfui`.
2. Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
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
- **SentinelBench**: monitor a synthetic transcript for blind spot risks.

## Screen recording tips

- Start with the app loading and the status tab showing available models.
- Show a basic chat prompt and a model response.
- Run SpecLab and explain this compares models on ethical value conflicts.
- Run SentinelBench and explain it uses a monitor-style evaluation on synthetic attack transcripts.
- Mention that the app adapts research ideas about model behavior and monitoring into a usable interactive demo.

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
