"""Static analysis of Python source using the built-in ``ast`` module.

Everything here is deterministic: no LLM is involved, so the facts
(function names, call relationships, control flow) are always real.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass, field


@dataclass
class FuncInfo:
    name: str
    lineno: int
    args: list[str]
    docstring: str | None
    calls: list[str] = field(default_factory=list)      # calls to other user-defined functions
    ext_calls: list[str] = field(default_factory=list)  # calls to builtins/libs
    loops: int = 0
    branches: int = 0
    returns: int = 0
    source: str = ""


@dataclass
class Analysis:
    functions: dict[str, FuncInfo]
    module_calls: list[str]
    imports: list[str]
    loc: int


def _call_name(node: ast.Call) -> str | None:
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return None


def analyze(source: str) -> Analysis:
    tree = ast.parse(source)
    lines = source.splitlines()
    defs: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defs.setdefault(node.name, node)

    funcs: dict[str, FuncInfo] = {}
    for name, node in defs.items():
        info = FuncInfo(
            name=name,
            lineno=node.lineno,
            args=[a.arg for a in node.args.args],
            docstring=ast.get_docstring(node),
            source="\n".join(lines[node.lineno - 1:node.end_lineno]),
        )
        for sub in ast.walk(node):
            if sub is node:
                continue
            if isinstance(sub, (ast.For, ast.While, ast.AsyncFor)):
                info.loops += 1
            elif isinstance(sub, (ast.If, ast.IfExp)):
                info.branches += 1
            elif isinstance(sub, ast.Return):
                info.returns += 1
            elif isinstance(sub, ast.Call):
                cn = _call_name(sub)
                if not cn:
                    continue
                target = info.calls if cn in defs else info.ext_calls
                if cn not in target:
                    target.append(cn)
        funcs[name] = info

    # calls made at module level (the "main flow")
    module_calls: list[str] = []
    for stmt in tree.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        for sub in ast.walk(stmt):
            if isinstance(sub, ast.Call):
                cn = _call_name(sub)
                if cn in defs and cn not in module_calls:
                    module_calls.append(cn)

    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)

    return Analysis(funcs, module_calls, sorted(set(imports)), len(lines))
