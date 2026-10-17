"""Syntax orchestration; intermediate values remain relational populations."""

import ast
from dataclasses import dataclass

from .engine import Config, Engine, ResourceLimit
from .numbers import decode, encode
from .operations import Value, add, divide, multiply, subtract


@dataclass
class Calculation:
    value: Value
    engine: Engine

    def observed(self) -> dict:
        return {"value": decode(self.value.population),
                "remainder": decode(self.value.remainder) if self.value.remainder else 0}


def calculate(expression: str, seed: int = 0, config: Config | None = None,
              trace: bool = False, answer: Value | None = None) -> Calculation:
    if len(expression) > 4096:
        raise ResourceLimit("Expression length limit exceeded")
    tree = ast.parse(expression, mode="eval")
    if len(list(ast.walk(tree))) > 512:
        raise ResourceLimit("Expression complexity limit exceeded")
    engine = Engine(seed, config, trace)

    def evaluate(node, depth=0) -> Value:
        if depth > 64:
            raise ResourceLimit("Expression nesting limit exceeded")
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return Value(engine.normalize(encode(node.value, engine)))
        if isinstance(node, ast.Name) and node.id == "ans" and answer is not None:
            # Reinstantiate the retained class without passing through a number.
            prior = answer.composable()
            return Value(engine.normalize([engine.relation(e.positive) for e in prior]))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = evaluate(node.operand, depth + 1).composable()
            return Value(engine.normalize(engine.invert(value)) if isinstance(node.op, ast.USub) else value)
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult,
                                                              ast.Div, ast.FloorDiv, ast.Mod)):
            left = evaluate(node.left, depth + 1).composable()
            right = evaluate(node.right, depth + 1).composable()
            if isinstance(node.op, ast.Add):
                return Value(add(left, right, engine))
            if isinstance(node.op, ast.Sub):
                return Value(subtract(left, right, engine))
            if isinstance(node.op, ast.Mult):
                return Value(multiply(left, right, engine))
            value = divide(left, right, engine)
            if isinstance(node.op, ast.FloorDiv):
                return Value(value.population)
            if isinstance(node.op, ast.Mod):
                return Value(value.remainder or [])
            return value
        raise ValueError("Supported syntax: integers, ans, + - * / // %, and parentheses")

    return Calculation(evaluate(tree.body), engine)
