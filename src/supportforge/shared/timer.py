"""
timer.py — Per-model session and request timing.

Tracks:
  - Session start/end times
  - Per-model API call latencies
  - Total tokens used (estimated)
  - Cost projection (for paid APIs)

Usage:
    start_session()
    log_usage("groq/llama3-8b", request_time_sec=0.234)
    summary = get_summary()
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


_session_start = None
_session_data = {
    "start_time": None,
    "end_time": None,
    "model_calls": []  # List of {model, latency_sec, tokens, timestamp}
}


def start_session() -> str:
    """Begin a new session. Return session ID."""
    global _session_start, _session_data
    _session_start = time.time()
    _session_data = {
        "start_time": datetime.now().isoformat(),
        "end_time": None,
        "model_calls": []
    }
    return datetime.now().isoformat()


def log_usage(
    model: str,
    request_time_sec: float,
    tokens_estimated: int = 0,
    provider_cost: float = 0.0
) -> None:
    """Log a single API call to the session.

    Args:
        model: Model identifier (e.g., 'groq/llama3-8b')
        request_time_sec: Time taken for API call in seconds
        tokens_estimated: Approximate tokens used (optional)
        provider_cost: Cost for this call in USD (optional)
    """
    if _session_start is None:
        start_session()

    _session_data["model_calls"].append({
        "model": model,
        "latency_sec": round(request_time_sec, 3),
        "tokens": tokens_estimated,
        "cost": round(provider_cost, 6),
        "timestamp": datetime.now().isoformat()
    })


def end_session() -> None:
    """Mark end of session."""
    global _session_data
    _session_data["end_time"] = datetime.now().isoformat()


def get_session_seconds() -> float:
    """Return elapsed seconds since session start."""
    if _session_start is None:
        return 0.0
    return time.time() - _session_start


def get_model_metrics(model: str) -> Dict[str, float]:
    """Get aggregated metrics for a specific model.

    Returns:
        {
            "call_count": int,
            "avg_latency_sec": float,
            "total_tokens": int,
            "total_cost": float,
            "total_time_sec": float
        }
    """
    calls = [c for c in _session_data["model_calls"] if c["model"] == model]

    if not calls:
        return {
            "call_count": 0,
            "avg_latency_sec": 0.0,
            "total_tokens": 0,
            "total_cost": 0.0,
            "total_time_sec": 0.0
        }

    total_latency = sum(c["latency_sec"] for c in calls)
    total_tokens = sum(c["tokens"] for c in calls)
    total_cost = sum(c["cost"] for c in calls)

    return {
        "call_count": len(calls),
        "avg_latency_sec": round(total_latency / len(calls), 3),
        "total_tokens": total_tokens,
        "total_cost": round(total_cost, 6),
        "total_time_sec": round(total_latency, 3)
    }


def get_all_model_metrics() -> Dict[str, Dict[str, float]]:
    """Get metrics for all models called in this session."""
    models = set(c["model"] for c in _session_data["model_calls"])
    return {model: get_model_metrics(model) for model in models}


def get_summary() -> str:
    """Return formatted summary of session metrics as markdown.

    Example output:
    ```
    ## Session Summary
    **Duration:** 45.23 sec

    | Model | Calls | Avg Latency | Total Tokens | Total Cost |
    |-------|-------|-------------|--------------|-----------|
    | groq/llama3-8b | 3 | 0.45s | 2140 | $0.000 |
    | ollama/mistral | 2 | 1.23s | 1850 | $0.000 |
    ```
    """
    duration = get_session_seconds()
    metrics = get_all_model_metrics()

    if not metrics:
        return "## Session Summary\nNo API calls logged yet."

    lines = [
        "## Session Summary",
        f"**Duration:** {duration:.2f} sec\n",
        "| Model | Calls | Avg Latency | Total Tokens | Total Cost |",
        "|-------|-------|-------------|--------------|-----------|"
    ]

    total_calls = 0
    total_cost = 0.0

    for model, data in sorted(metrics.items()):
        calls = data["call_count"]
        avg_latency = data["avg_latency_sec"]
        tokens = data["total_tokens"]
        cost = data["total_cost"]

        total_calls += calls
        total_cost += cost

        lines.append(
            f"| {model} | {calls} | {avg_latency:.3f}s | {tokens} | ${cost:.6f} |"
        )

    lines.append(f"\n**Total Calls:** {total_calls} | **Total Cost:** ${total_cost:.6f}")

    return "\n".join(lines)


def save_session(filename: Optional[str] = None) -> str:
    """Save session data to JSON file. Return filename."""
    if filename is None:
        filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    end_session()
    path = Path(filename)
    path.write_text(json.dumps(_session_data, indent=2))
    return str(path)


def load_session(filename: str) -> Dict:
    """Load session data from JSON file."""
    global _session_data
    path = Path(filename)
    _session_data = json.loads(path.read_text())
    return _session_data
