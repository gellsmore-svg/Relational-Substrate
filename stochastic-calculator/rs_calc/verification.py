"""Conventional arithmetic ORACLE. Mechanism modules must never import this."""

import ast


def expected_binary(op: str, a: int, b: int) -> dict:
    if op == "add":
        return {"value": a + b, "remainder": 0}
    if op == "sub":
        return {"value": a - b, "remainder": 0}
    if op == "mul":
        return {"value": a * b, "remainder": 0}
    if op == "div":
        q = abs(a) // abs(b)
        if (a < 0) != (b < 0):
            q = -q
        return {"value": q, "remainder": a - b * q}
    raise ValueError("Unknown operation")


def audit_sources(root) -> list[str]:
    findings = []
    for name in ["engine.py", "operations.py", "numbers.py", "calculator.py", "radix.py", "proposal_kernel.py"]:
        path = root / "rs_calc" / name
        if not path.exists():
            continue
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.ImportFrom) and node.module and any(
                    word in node.module for word in ("verification", "metrics", "experiments", "constraint_lab")):
                findings.append(f"{name}:{node.lineno}: measuring instrument imported by mechanism")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {
                    "eval", "exec", "compile", "sum", "divmod"}:
                findings.append(f"{name}:{node.lineno}: forbidden mechanism helper {node.func.id}")
            if name == "operations.py" and isinstance(node, ast.BinOp) and not isinstance(node.op, ast.BitOr):
                findings.append(f"{name}:{node.lineno}: numeric binary operation needs audit")
    return findings
