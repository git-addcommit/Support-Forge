"""
tools.py — Helper tools for the Gradio UI.

Tools:
  1. Calculator — Safely evaluate math expressions
  2. Web Search — Mock or real web search integration
  3. File Reader — Sandboxed file listing and reading

Each tool is designed to be called from a Gradio button and return
a user-friendly markdown string.
"""

import ast
import math
import os
from pathlib import Path
from typing import Optional


# ── Configuration ──────────────────────────────────────────────────────────

# Sandbox directory for file reader (prevent path traversal)
SANDBOX_DIR = Path(__file__).parent / "samples"
SANDBOX_DIR.mkdir(exist_ok=True)

# Max file size to read (prevent loading huge files)
MAX_FILE_SIZE = 1_000_000  # 1 MB


# ── Calculator Tool ────────────────────────────────────────────────────────

def run_calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely.

    Allowed functions: sqrt, sin, cos, tan, log, exp
    Blocked: __import__, open, exec, etc.

    Args:
        expression: Math expression (e.g., "sqrt(16) + 2**3")

    Returns:
        Markdown-formatted result or error message.
    """
    if not expression or not expression.strip():
        return "❌ **Calculator:** Please enter an expression (e.g., `2 + 2` or `sqrt(9)`)"

    try:
        # Parse to check for dangerous patterns
        tree = ast.parse(expression, mode='eval')

        safe_names = {'sqrt', 'sin', 'cos', 'tan', 'log', 'exp', 'abs', 'round', 'pi', 'e'}
        allowed_binary_ops = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv)
        allowed_unary_ops = (ast.USub,)
        allowed_nodes = (
            ast.Expression,
            ast.BinOp,
            ast.UnaryOp,
            ast.Call,
            ast.Name,
            ast.Constant,
            ast.Load,
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.Pow,
            ast.Mod,
            ast.FloorDiv,
            ast.USub,
        )

        for node in ast.walk(tree):
            if not isinstance(node, allowed_nodes):
                raise ValueError(f"Node type {type(node).__name__} is not allowed")

            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name):
                    raise ValueError("Attribute and method calls are not allowed")
                if node.func.id not in safe_names:
                    raise ValueError(f"Function '{node.func.id}' is not allowed")
            elif isinstance(node, ast.Name):
                if node.id not in safe_names:
                    raise ValueError(f"Name '{node.id}' is not allowed")
            elif isinstance(node, ast.BinOp):
                if not isinstance(node.op, allowed_binary_ops):
                    raise ValueError(f"Operator '{type(node.op).__name__}' is not allowed")
            elif isinstance(node, ast.UnaryOp):
                if not isinstance(node.op, allowed_unary_ops):
                    raise ValueError(f"Unary operator '{type(node.op).__name__}' is not allowed")
                if isinstance(node.operand, ast.UnaryOp):
                    raise ValueError("Nested unary operators are not allowed")
                if isinstance(node.op, ast.UAdd):
                    raise ValueError("Unary plus is not allowed")

        # Safe namespace: math functions only, no builtins
        safe_dict = {
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'exp': math.exp,
            'abs': abs,
            'round': round,
            'pi': math.pi,
            'e': math.e,
        }

        result = eval(expression, {"__builtins__": {}}, safe_dict)

        return f"**Result:** `{result}`"

    except ValueError as e:
        return f"❌ **Calculator:** {str(e)}"
    except SyntaxError:
        return f"❌ **Calculator:** Invalid expression. Check your syntax."
    except ZeroDivisionError:
        return f"❌ **Calculator:** Division by zero"
    except Exception as e:
        return f"❌ **Calculator:** Error — {type(e).__name__}: {str(e)}"


# ── Web Search Tool ────────────────────────────────────────────────────────

def run_web_search(query: str) -> str:
    """Mock web search (TODO: integrate real API).

    Placeholder for now; future integration points:
      - DuckDuckGo API (free)
      - SerpAPI (limited free tier)
      - Bing Search API

    Args:
        query: Search query

    Returns:
        Markdown-formatted search results.
    """
    if not query or not query.strip():
        return "🔍 **Web Search:** Please enter a search query."

    # TODO: Replace with real API call
    # For now, return mock results
    return f"""🔍 **Web Search:** "{query}"

*Mock results — Coming soon with DuckDuckGo API integration.*

**Planned features:**
- Real-time search results
- Source attribution
- Automatic synthesis by Claude
- Cost tracking for API calls

**To integrate:**
1. Get free API key from duckduckgo.com or bing.com
2. Add to .env: `SEARCH_API_KEY=...`
3. Implement `_call_search_api()` below

---
"""


def _call_search_api(query: str, api_key: str) -> list[dict]:
    """Placeholder for real search API integration.

    Example with DuckDuckGo (requires ddg-python package):

    ```python
    from duckduckgo_search import DDGS

    def _call_search_api(query: str, api_key: str = None) -> list[dict]:
        results = []
        try:
            with DDGS() as ddgs:
                for result in ddgs.text(query, max_results=5):
                    results.append({
                        'title': result['title'],
                        'body': result['body'],
                        'href': result['href']
                    })
        except Exception as e:
            print(f"Search error: {e}")
        return results
    ```

    Then update run_web_search() to use it:

    ```python
    results = _call_search_api(query)
    md = f"## Search results for '{query}'\n\n"
    for r in results:
        md += f"- [{r['title']}]({r['href']})\n  {r['body']}\n\n"
    return md
    ```
    """
    return []


# ── File Reader Tool ──────────────────────────────────────────────────────

def run_file_reader(file_path: str) -> str:
    """Read or list files in the sandbox directory.

    Security:
      - Only reads from SANDBOX_DIR and subdirs
      - Refuses to read files > MAX_FILE_SIZE
      - Returns error for symlinks to prevent escapes

    Args:
        file_path: Path relative to SANDBOX_DIR, or absolute path within sandbox

    Returns:
        Markdown-formatted file content or directory listing, or error message.
    """
    if not file_path or not file_path.strip():
        return f"📄 **File Reader:** List files in `{SANDBOX_DIR}` with a path."

    # Resolve path and ensure it's in sandbox
    try:
        target = Path(file_path).resolve()
        sandbox_resolved = SANDBOX_DIR.resolve()

        # If the user provided a path outside the sandbox, reject it.
        try:
            target.relative_to(sandbox_resolved)
        except ValueError:
            # Path is outside sandbox
            return f"❌ **File Reader:** Access denied. Files must be in `{SANDBOX_DIR}`"

        # Refuse symlinks
        if target.is_symlink():
            return f"❌ **File Reader:** Symlinks not allowed"

        if target.is_dir():
            # List files in directory
            try:
                files = [f.name for f in target.iterdir() if not f.name.startswith('.')]
                if not files:
                    return f"📁 **Directory:** `{target.name}` is empty"
                file_list = "\n".join(f"- `{f}`" for f in sorted(files))
                return f"📁 **Directory:** `{target.name}`\n\n{file_list}"
            except PermissionError:
                return f"❌ **File Reader:** Permission denied"

        elif target.is_file():
            # Read file content
            if target.stat().st_size > MAX_FILE_SIZE:
                # File too large; show preview
                with open(target, 'r', errors='ignore') as f:
                    preview = f.read(500)
                return f"""📄 **File:** `{target.name}`

*File too large ({target.stat().st_size / 1024:.0f} KB); showing preview.*

```
{preview}
...
```

_(Increase MAX_FILE_SIZE if you need more)_
"""
            else:
                # Read full content
                with open(target, 'r', errors='ignore') as f:
                    content = f.read()

                # Wrap in code block for readability
                return f"""📄 **File:** `{target.name}`

```
{content}
```
"""
        else:
            return f"❌ **File Reader:** `{file_path}` not found"

    except Exception as e:
        return f"❌ **File Reader:** Error — {type(e).__name__}: {str(e)}"


# ── Utility function for Gradio integration ────────────────────────────────

def get_tool_descriptions() -> dict[str, str]:
    """Return descriptions of available tools for UI tooltip."""
    return {
        "calculator": "Evaluate math expressions (e.g., sqrt(16) + 2**3)",
        "web_search": "Search the web for information (coming soon with real API)",
        "file_reader": f"Read files from {SANDBOX_DIR} directory",
    }
