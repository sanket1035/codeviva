"""Regenerate examples/<sample>/ from samples/*.py in offline (AST-only) mode.

Run from the repo root:  python scripts/generate_examples.py
Offline mode is used on purpose so the committed output is reproducible and
needs no API key. LLM-written explanations are not committed here.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.pop("GROQ_API_KEY", None)

from codeviva.analyzer import analyze  # noqa: E402
from codeviva.diagram import call_graph  # noqa: E402
from codeviva.llm import offline_fallback  # noqa: E402
from codeviva.report import explanation_markdown, viva_markdown  # noqa: E402
from codeviva.verify import check  # noqa: E402


def main() -> None:
    for src in sorted((ROOT / "samples").glob("*.py")):
        a = analyze(src.read_text(encoding="utf-8"))
        res = offline_fallback(a)
        v = check(res, a)
        out = ROOT / "examples" / src.stem
        out.mkdir(parents=True, exist_ok=True)
        (out / "diagram.mmd").write_text(call_graph(a) + "\n", encoding="utf-8")
        (out / "explanation.md").write_text(explanation_markdown(res, a) + "\n", encoding="utf-8")
        (out / "viva.md").write_text(viva_markdown(res) + "\n", encoding="utf-8")
        loops = sum(f.loops for f in a.functions.values())
        print(f"{src.name}: {len(a.functions)} functions, {loops} loops, "
              f"{len(res['viva'])} viva questions, grounded={v['grounded']}")


if __name__ == "__main__":
    main()
