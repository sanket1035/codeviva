"""Hallucination check: function names in LLM text must exist in the code."""
from codeviva.analyzer import analyze
from codeviva.verify import check

SRC = "def deposit(b, a):\n    return b + a\n\ndef withdraw(b, a):\n    return b - a\n"


def _res(summary="", functions=None, viva=None):
    return {"summary": summary, "functions": functions or {}, "viva": viva or []}


def test_real_names_are_grounded():
    out = check(_res("It uses `deposit()` and `withdraw()`."), analyze(SRC))
    assert out["grounded"] and out["hallucinated"] == []
    assert out["checked"] == 2


def test_invented_name_in_summary_is_flagged():
    out = check(_res("It calls `transfer_money()`."), analyze(SRC))
    assert out["hallucinated"] == ["transfer_money"] and not out["grounded"]


def test_invented_name_in_viva_question_and_answer_is_flagged():
    viva = [{"q": "What does audit() do?", "a": "It wraps log_event()."}]
    out = check(_res(viva=viva), analyze(SRC))
    assert out["hallucinated"] == ["audit", "log_event"]


def test_invented_key_in_function_explanations_is_flagged():
    out = check(_res(functions={"deposit": "ok", "ghost": "invented"}), analyze(SRC))
    assert out["hallucinated"] == ["ghost"]


def test_hallucinated_names_are_sorted_and_unique():
    out = check(_res("zeta() zeta() alpha()"), analyze(SRC))
    assert out["hallucinated"] == ["alpha", "zeta"]


def test_builtins_are_not_flagged():
    out = check(_res("It calls `len()` and print()."), analyze(SRC))
    assert out["grounded"]


def test_empty_result_is_grounded():
    out = check({}, analyze(SRC))
    assert out == {"checked": 0, "hallucinated": [], "grounded": True}


def test_names_are_case_sensitive():
    out = check(_res("It calls Deposit()."), analyze(SRC))
    assert out["hallucinated"] == ["Deposit"]


def test_known_limitation_name_without_parentheses_is_not_checked():
    out = check(_res("It calls transfer_money to move cash."), analyze(SRC))
    assert out["grounded"]  # missed: only `name()` patterns are detected


def test_known_limitation_invented_name_equal_to_builtin_passes():
    out = check(_res("It calls sorted()."), analyze("def f():\n    pass\n"))
    assert out["grounded"]
