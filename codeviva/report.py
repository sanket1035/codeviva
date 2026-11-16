"""Markdown rendering of an explanation result (used by the app and by examples)."""
from __future__ import annotations

from .analyzer import Analysis


def viva_markdown(res: dict) -> str:
    return "\n\n".join(
        f"**Q{i}. {x['q']}**\n\n{x['a']}" for i, x in enumerate(res.get("viva", []), 1)
    )


def explanation_markdown(res: dict, a: Analysis) -> str:
    parts = [res.get("summary", "")]
    for name, text in res.get("functions", {}).items():
        line = a.functions[name].lineno if name in a.functions else "?"
        parts.append(f"### `{name}()` (line {line})\n\n{text}")
    return "\n\n".join(parts)
