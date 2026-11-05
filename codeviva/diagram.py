"""Turns an Analysis into Mermaid text. Pure Python, no LLM."""
from __future__ import annotations

from .analyzer import Analysis


def call_graph(a: Analysis) -> str:
    out = ["flowchart LR"]
    if a.module_calls:
        out.append('    MAIN(["▶ program start"]):::entry')
    for f in a.functions.values():
        label = f"{f.name}({', '.join(f.args)})"
        shape = f'{f.name}["{label}"]'
        if f.loops:
            shape += f":::looped"
        out.append(f"    {shape}")
    for c in a.module_calls:
        out.append(f"    MAIN --> {c}")
    for f in a.functions.values():
        for c in f.calls:
            arrow = "-.->" if c == f.name else "-->"   # dotted = recursion
            out.append(f"    {f.name} {arrow} {c}")
    out.append("    classDef entry fill:#111,stroke:#111,color:#fff")
    out.append("    classDef looped fill:#f6d9a8,stroke:#b45309,color:#451a03")
    return "\n".join(out)


def function_flow(name: str, a: Analysis) -> str:
    """Mini flowchart for one function: args -> loops/branches -> calls -> return."""
    f = a.functions[name]
    n = ["flowchart LR", f'    s(["{name}"]) --> i["input: {", ".join(f.args) or "none"}"]']
    prev = "i"
    k = 0
    def add(label, shape="[{}]"):
        nonlocal prev, k
        k += 1
        nid = f"n{k}"
        n.append(f"    {prev} --> {nid}{shape.format(chr(34)+label+chr(34))}")
        prev = nid
    if f.branches:
        add(f"{f.branches} decision(s)", "{{{}}}")
    if f.loops:
        add(f"{f.loops} loop(s)")
    for c in f.calls:
        add(f"calls {c}()")
    add("return" if f.returns else "end", "([{}])")
    return "\n".join(n)
