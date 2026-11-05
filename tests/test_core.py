from codeviva.analyzer import analyze
from codeviva.diagram import call_graph
from codeviva.llm import offline_fallback
from codeviva.verify import check

SRC = open("samples/bank_account.py", encoding="utf-8").read()


def test_functions_and_calls():
    a = analyze(SRC)
    assert {"deposit", "withdraw", "factorial", "main"} <= set(a.functions)
    assert "validate_amount" in a.functions["deposit"].calls
    assert a.module_calls == ["main"]


def test_loops_and_recursion():
    a = analyze(SRC)
    assert a.functions["interest"].loops == 1
    assert "factorial" in a.functions["factorial"].calls


def test_mermaid_has_edges():
    g = call_graph(analyze(SRC))
    assert g.startswith("flowchart LR")
    assert "deposit --> validate_amount" in g
    assert "factorial -.-> factorial" in g


def test_verify_catches_hallucination():
    a = analyze(SRC)
    res = offline_fallback(a)
    assert check(res, a)["grounded"]
    res["summary"] += " It also calls `transfer_money()`."
    out = check(res, a)
    assert out["hallucinated"] == ["transfer_money"]
