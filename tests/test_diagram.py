from codeviva.analyzer import analyze
from codeviva.diagram import call_graph, function_flow

SRC = "def a(x):\n    for i in x:\n        pass\n    b()\n\ndef b():\n    return b()\n\na([])\n"


def test_main_node_only_when_module_calls_exist():
    assert "MAIN" in call_graph(analyze(SRC))
    assert "MAIN" not in call_graph(analyze("def a():\n    pass\n"))


def test_loop_function_is_highlighted_and_edges_drawn():
    g = call_graph(analyze(SRC))
    assert 'a["a(x)"]:::looped' in g
    assert "a --> b" in g and "MAIN --> a" in g


def test_recursion_is_dotted():
    assert "b -.-> b" in call_graph(analyze(SRC))


def test_function_flow_lists_loops_calls_and_return():
    f = function_flow("a", analyze(SRC))
    assert "1 loop(s)" in f and "calls b()" in f and "end" in f
    assert "return" in function_flow("b", analyze(SRC))
