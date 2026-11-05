"""Hallucination check: every function the LLM names must exist in the AST."""
from __future__ import annotations

import builtins
import re

from .analyzer import Analysis

_CALL = re.compile(r"`?\b([A-Za-z_][A-Za-z0-9_]*)\(\)`?")


def check(result: dict, a: Analysis) -> dict:
    """Return which function names in the LLM text do not exist in the code."""
    known = set(a.functions)
    parts = [result.get("summary", "")]
    parts += list(result.get("functions", {}).values())
    for item in result.get("viva", []):
        parts += [item.get("q", ""), item.get("a", "")]
    text = " ".join(parts)
    named = set(_CALL.findall(text)) | set(result.get("functions", {}))
    unknown = sorted(n for n in named
                     if n not in known and not hasattr(builtins, n))
    return {"checked": len(named), "hallucinated": unknown,
            "grounded": not unknown}
