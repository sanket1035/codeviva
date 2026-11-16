"""AST parser: functions, arguments, calls, loops, decisions, imports."""
import pytest

from codeviva.analyzer import analyze


def test_empty_source_has_no_functions():
    a = analyze("")
    assert a.functions == {} and a.module_calls == [] and a.loc == 0


def test_syntax_error_is_raised_with_line_number():
    with pytest.raises(SyntaxError) as e:
        analyze("x = 1\ndef f(:\n")
    assert e.value.lineno == 2


def test_arguments_docstring_and_line_number():
    a = analyze('def add(x, y):\n    """Add two numbers."""\n    return x + y\n')
    f = a.functions["add"]
    assert f.args == ["x", "y"]
    assert f.docstring == "Add two numbers."
    assert f.lineno == 1
    assert f.returns == 1


def test_user_calls_and_external_calls_are_separated():
    a = analyze("def a():\n    print(1)\n    b()\n\ndef b():\n    pass\n")
    assert a.functions["a"].calls == ["b"]
    assert a.functions["a"].ext_calls == ["print"]


def test_calls_are_deduplicated():
    a = analyze("def a():\n    b()\n    b()\n\ndef b():\n    pass\n")
    assert a.functions["a"].calls == ["b"]


def test_direct_recursion_is_a_self_call():
    a = analyze("def f(n):\n    return f(n - 1) if n else 0\n")
    assert a.functions["f"].calls == ["f"]
    assert a.functions["f"].branches == 1  # the conditional expression


def test_loop_and_branch_counts():
    src = (
        "def f(xs):\n"
        "    for x in xs:\n"
        "        if x:\n"
        "            pass\n"
        "    while xs:\n"
        "        xs.pop()\n"
        "    return 1\n"
    )
    f = analyze(src).functions["f"]
    assert (f.loops, f.branches) == (2, 1)


def test_elif_chain_counts_each_branch():
    src = "def g(a):\n    if a > 2:\n        return 1\n    elif a > 1:\n        return 2\n    return 3\n"
    assert analyze(src).functions["g"].branches == 2


def test_async_functions_are_found():
    a = analyze("async def f():\n    await g()\n\nasync def g():\n    pass\n")
    assert set(a.functions) == {"f", "g"}
    assert a.functions["f"].calls == ["g"]


def test_nested_function_is_listed_and_called_by_parent():
    a = analyze("def outer():\n    def inner():\n        pass\n    inner()\n")
    assert set(a.functions) == {"outer", "inner"}
    assert a.functions["outer"].calls == ["inner"]


def test_module_calls_only_include_user_functions_in_order():
    a = analyze("def a():\n    pass\n\ndef b():\n    pass\n\nprint('x')\nb()\na()\n")
    assert a.module_calls == ["b", "a"]


def test_calls_inside_function_bodies_are_not_module_calls():
    a = analyze("def a():\n    pass\n\ndef b():\n    a()\n")
    assert a.module_calls == []


def test_imports_are_sorted_and_unique():
    a = analyze("import os\nimport math, os\nfrom collections import deque\n")
    assert a.imports == ["collections", "math", "os"]


def test_function_source_is_captured():
    a = analyze("def a():\n    return 1\n\nx = 2\n")
    assert a.functions["a"].source == "def a():\n    return 1"


def test_self_method_call_is_a_user_call():
    src = "class A:\n    def a(self):\n        self.b()\n    def b(self):\n        pass\n"
    assert analyze(src).functions["a"].calls == ["b"]


def test_method_call_on_other_object_is_not_guessed_as_user_call():
    # ``items.pop()`` must not be read as a call to a user function named ``pop``
    src = "def pop():\n    pass\n\ndef f(items):\n    items.pop()\n"
    f = analyze(src).functions["f"]
    assert f.calls == []
    assert f.ext_calls == ["items.pop"]


def test_method_named_like_list_method_is_not_reported_as_recursion(sample):
    a = analyze(sample("stack_queue"))
    assert "pop" not in a.functions["pop"].calls
    assert a.functions["pop"].calls == ["is_empty"]


def test_known_limitation_same_method_name_in_two_classes_is_merged():
    src = "class A:\n    def run(self):\n        return 1\nclass B:\n    def run(self):\n        return 2\n"
    a = analyze(src)
    assert list(a.functions) == ["run"]
    assert a.functions["run"].source.endswith("return 1")  # first definition wins
