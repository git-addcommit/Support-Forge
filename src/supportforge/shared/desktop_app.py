"""
cipher-fellows — Desktop GUI (PySimpleGUI)

A native desktop application for AI model comparison and research.
More lightweight than web UI, runs offline with local models.

Run:
    python desktop_app.py
"""

import PySimpleGUI as sg
import json
import os
import threading
from pathlib import Path
from datetime import datetime

# ── Import our modules ─────────────────────────────────────────────────────
try:
    from timer import (
        start_session, log_usage, get_session_seconds,
        get_summary as timer_summary
    )
    from tools import run_calculator, run_web_search, run_file_reader
except ImportError as e:
    print(f"WARNING: Import warning — timer/tools modules not found: {e}")

# ── Load .env ──────────────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Simple provider router ──────────────────────────────────────────────────

def simple_call(model: str, system: str, user: str) -> str:
    """Simplified model call for desktop app."""
    if "ollama" in model:
        import urllib.request, json as json_lib
        try:
            payload = {
                "model": model.split("/")[1] if "/" in model else "llama2",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                "stream": False
            }
            req = urllib.request.Request(
                "http://localhost:11434/api/chat",
                data=json_lib.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=60) as r:
                return json_lib.loads(r.read())["message"]["content"]
        except Exception as e:
            return f"Error: {e}"
    return "Model not supported in desktop mode. Use web UI for Groq/Anthropic/NIM."


# ── PySimpleGUI Theme & Layout ─────────────────────────────────────────────

sg.theme("Dark")
sg.set_options(font=("Consolas", 11), element_padding=((8, 8), (6, 6)))

MODELS = [
    "ollama/llama2",
    "ollama/mistral",
    "ollama/neural-chat"
]


def build_chat_window():
    """Build chat interface."""
    layout = [
        [sg.Text("cipher-fellows — Desktop Research Chat", font=("Arial", 16, "bold"))],
        [sg.Text("A lightweight companion for local model exploration and notes.")],
        [sg.Text("Model:"), sg.Combo(MODELS, default_value="ollama/llama2", key="-MODEL-", readonly=True, size=(30, 1))],
        [sg.Text("System prompt:"), sg.Button("Reset prompt", key="-RESET-PROMPT-")],
        [sg.Multiline(
            default_text="You are a thoughtful, human-style research assistant. Keep the tone natural, explain clearly, and stay concise.",
            size=(60, 4),
            key="-SYSTEM-"
        )],
        [sg.Text("Conversation history:" )],
        [sg.Multiline(
            size=(60, 16),
            key="-CHAT-",
            disabled=True,
            background_color="#121212",
            text_color="#E0E0E0",
            autoscroll=True
        )],
        [sg.Text("Message:"), sg.InputText(size=(46, 1), key="-USER-MSG-")],
        [sg.Button("Send", size=(10, 1)), sg.Button("Clear chat", size=(10, 1)), sg.Button("Save chat", size=(10, 1)), sg.Button("Exit", size=(10, 1))],
        [sg.Button("Calculator", size=(12, 1)), sg.Button("Search", size=(12, 1)), sg.Button("Metrics", size=(12, 1)), sg.Button("Files", size=(12, 1))]
    ]
    return sg.Window("cipher-fellows Desktop", layout, finalize=True, resizable=True)


def build_tools_window():
    """Build tools interface."""
    layout = [
        [sg.Text("cipher-fellows Tools", font=("Arial", 14, "bold"))],
        [sg.TabGroup([
            sg.Tab("Calculator", [
                [sg.Text("Expression:")],
                [sg.InputText(size=(40, 1), key="-CALC-EXPR-")],
                [sg.Button("Calculate"), sg.Button("Clear")],
                [sg.Multiline(
                    size=(40, 10),
                    key="-CALC-OUT-",
                    disabled=True
                )]
            ]),
            sg.Tab("Web Search", [
                [sg.Text("Query:")],
                [sg.InputText(size=(40, 1), key="-SEARCH-QUERY-")],
                [sg.Button("Search"), sg.Button("Clear")],
                [sg.Multiline(
                    size=(40, 10),
                    key="-SEARCH-OUT-",
                    disabled=True
                )]
            ]),
            sg.Tab("File Reader", [
                [sg.Text("Select or drag a file to preview")],
                [sg.InputText(size=(30, 1), key="-FILE-PATH-", enable_events=True, tooltip="Drop a file here or click Browse", do_not_clear=False, drop_target=True), sg.FileBrowse(file_types=("Text Files", "*.txt;*.md;*.json;*.csv"))],
                [sg.Button("Read"), sg.Button("Clear")],
                [sg.Multiline(
                    size=(40, 10),
                    key="-FILE-OUT-",
                    disabled=True
                )]
            ]),
        ])]
    ]
    return sg.Window("Tools", layout)


def build_metrics_window():
    """Build metrics display."""
    try:
        metrics = timer_summary()
    except:
        metrics = "No metrics yet."

    layout = [
        [sg.Text("Session Metrics", font=("Arial", 14, "bold"))],
        [sg.Multiline(
            default_text=metrics,
            size=(60, 20),
            disabled=True,
            background_color="#1a1a1a",
            text_color="#0F0",
            key="-METRICS-OUT-"
        )],
        [sg.Button("Refresh"), sg.Button("Save"), sg.Button("Close")]
    ]
    return sg.Window("Metrics", layout)


def main():
    """Main event loop."""
    start_session()

    window = build_chat_window()
    chat_history = ""

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

        elif event == "Send":
            user_msg = values["-USER-MSG-"]
            if user_msg.strip():
                window["-CHAT-"].print(f"You: {user_msg}")

                model = values["-MODEL-"]
                system = values["-SYSTEM-"]
                response = simple_call(model, system, user_msg)
                log_usage(model, 0.5)

                window["-CHAT-"].print(f"Bot: {response}\n")
                window["-USER-MSG-"].update("")

        elif event == "Clear chat":
            window["-CHAT-"].update("")

        elif event == "Save chat":
            text = values["-CHAT-"]
            if text.strip():
                fname = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                Path(fname).write_text(text)
                sg.popup_ok(f"Conversation saved to {fname}")

        elif event == "Reset prompt":
            window["-SYSTEM-"].update(
                "You are a thoughtful, human-style research assistant. Keep the tone natural, explain clearly, and stay concise."
            )

        elif event == "Calculator":
            tools_win = build_tools_window()
            while True:
                t_event, t_values = tools_win.read()
                if t_event == sg.WINDOW_CLOSED:
                    break
                if t_event == "Calculate":
                    result = run_calculator(t_values["-CALC-EXPR-"])
                    tools_win["-CALC-OUT-"].update(result)
                if t_event == "Clear":
                    tools_win["-CALC-EXPR-"].update("")
                    tools_win["-CALC-OUT-"].update("")
            tools_win.close()

        elif event == "Search":
            tools_win = build_tools_window()
            while True:
                t_event, t_values = tools_win.read()
                if t_event == sg.WINDOW_CLOSED:
                    break
                if t_event == "Search":
                    result = run_web_search(t_values["-SEARCH-QUERY-"])
                    tools_win["-SEARCH-OUT-"].update(result)
                if t_event == "Clear":
                    tools_win["-SEARCH-QUERY-"].update("")
                    tools_win["-SEARCH-OUT-"].update("")
            tools_win.close()

        elif event == "Files":
            tools_win = build_tools_window()
            while True:
                t_event, t_values = tools_win.read()
                if t_event == sg.WINDOW_CLOSED:
                    break
                if t_event == "Read":
                    file_path = t_values["-FILE-PATH-"]
                    if file_path:
                        try:
                            p = Path(file_path)
                            if p.is_dir():
                                files = [f.name for f in p.iterdir() if not f.name.startswith('.')]
                                result = "\n".join(sorted(files)) if files else "Directory is empty."
                            else:
                                with open(p, "r", errors="ignore") as f:
                                    content = f.read(1200)
                                size = p.stat().st_size
                                if size > 1200:
                                    result = f"Preview of {p.name} ({size // 1024} KB):\n\n{content}\n\n... file truncated ..."
                                else:
                                    result = content
                        except Exception as e:
                            result = f"Error reading file: {type(e).__name__}: {e}"
                    else:
                        result = "Select or drag a file to preview."
                    tools_win["-FILE-OUT-"].update(result)
                if t_event == "Clear":
                    tools_win["-FILE-PATH-"].update("")
                    tools_win["-FILE-OUT-"].update("")
            tools_win.close()

        elif event == "Metrics":
            metrics_win = build_metrics_window()
            while True:
                m_event, m_values = metrics_win.read()
                if m_event == sg.WINDOW_CLOSED or m_event == "Close":
                    break
                if m_event == "Refresh":
                    metrics = timer_summary()
                    metrics_win["-METRICS-OUT-"].update(metrics)
                if m_event == "Save":
                    fname = f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    Path(fname).write_text(timer_summary())
                    sg.popup_ok(f"Saved to {fname}")
            metrics_win.close()

    window.close()


if __name__ == "__main__":
    main()
