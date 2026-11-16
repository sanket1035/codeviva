"""Every bundled sample must analyse, run, and pass the offline pipeline."""
import subprocess
import sys
from pathlib import Path

import pytest

from codeviva.analyzer import analyze
from codeviva.diagram import call_graph, function_flow
from codeviva.llm import offline_fallback
from codeviva.report import explanation_markdown, viva_markdown
from codeviva.verify import check

SAMPLES = sorted((Path(__file__).resolve().parent.parent / "samples").glob("*.py"))


def test_at_least_four_samples():
    assert len(SAMPLES) >= 4


@pytest.mark.parametrize("path", SAMPLES, ids=lambda p: p.stem)
def test_pipeline_on_sample(path):
    a = analyze(path.read_text(encoding="utf-8"))
    assert a.functions
    res = offline_fallback(a)
    assert 1 <= len(res["viva"]) <= 10
    assert check(res, a)["grounded"]
    g = call_graph(a)
    assert g.startswith("flowchart LR")
    for name in a.functions:
        assert name in g
        assert function_flow(name, a).startswith("flowchart LR")
    assert "Q1." in viva_markdown(res)
    assert explanation_markdown(res, a)


@pytest.mark.parametrize("path", SAMPLES, ids=lambda p: p.stem)
def test_sample_actually_runs(path):
    r = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, timeout=30)
    assert r.returncode == 0, r.stderr


def test_generated_examples_are_up_to_date():
    """examples/ must match what scripts/generate_examples.py produces."""
    root = SAMPLES[0].parent.parent
    for path in SAMPLES:
        a = analyze(path.read_text(encoding="utf-8"))
        res = offline_fallback(a)
        out = root / "examples" / path.stem
        assert (out / "diagram.mmd").read_text(encoding="utf-8") == call_graph(a) + "\n"
        assert (out / "viva.md").read_text(encoding="utf-8") == viva_markdown(res) + "\n"
