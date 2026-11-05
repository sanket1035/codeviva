"""Groq wrapper. The LLM only *explains*; facts come from the AST."""
from __future__ import annotations

import json
import os

from .analyzer import Analysis

MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def _facts(a: Analysis) -> str:
    rows = []
    for f in a.functions.values():
        rows.append({
            "name": f.name, "args": f.args, "calls": f.calls,
            "loops": f.loops, "branches": f.branches,
            "docstring": f.docstring, "code": f.source,
        })
    return json.dumps({"imports": a.imports, "functions": rows}, indent=1)


def _client():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        return None
    from groq import Groq
    return Groq(api_key=key)


def llm_available() -> bool:
    return bool(os.getenv("GROQ_API_KEY"))


def explain_and_quiz(a: Analysis, language: str = "English") -> dict:
    """Returns {"summary": str, "functions": {name: str}, "viva": [{"q","a"}]}."""
    client = _client()
    if client is None:
        return offline_fallback(a)
    system = (
        "You are a patient lab teacher. You are given VERIFIED facts about a Python "
        "program extracted by static analysis. Only mention functions that appear in "
        "the facts. Reply with JSON only: "
        '{"summary": str, "functions": {"<name>": "<2-3 simple sentences>"}, '
        '"viva": [{"q": str, "a": str}] } with exactly 10 viva questions, easy to hard. '
        f"Write in {language}."
    )
    resp = client.chat.completions.create(
        model=MODEL, temperature=0.2,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": _facts(a)}],
    )
    return json.loads(resp.choices[0].message.content)


def offline_fallback(a: Analysis) -> dict:
    """No API key: build plain explanations straight from the AST (demo mode)."""
    funcs = {}
    for f in a.functions.values():
        bits = [f"`{f.name}` takes {len(f.args)} input(s)" + (f" ({', '.join(f.args)})" if f.args else "") + "."]
        if f.docstring:
            bits.append(f.docstring.splitlines()[0])
        if f.loops:
            bits.append(f"It uses {f.loops} loop(s).")
        if f.branches:
            bits.append(f"It makes {f.branches} decision(s) with if/else.")
        if f.calls:
            bits.append("It calls " + ", ".join(f"`{c}`" for c in f.calls) + ".")
        funcs[f.name] = " ".join(bits)
    viva = []
    for f in a.functions.values():
        viva.append({"q": f"What does the function `{f.name}` do?", "a": funcs[f.name]})
        if f.calls:
            viva.append({"q": f"Which functions does `{f.name}` call and why?",
                         "a": f"It calls {', '.join(f.calls)}."})
    return {"summary": f"Program with {len(a.functions)} function(s) and {a.loc} lines. "
                       "(Offline mode: add GROQ_API_KEY for AI explanations.)",
            "functions": funcs, "viva": viva[:10]}
