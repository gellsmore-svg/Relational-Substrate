"""Planner and disk-book tests. They do not run the generation census."""

from __future__ import annotations

from fractions import Fraction

import pytest

from rs_constraint_lab.constraints import parse_expression
from rs_constraint_lab.gen007_exec import DiskBook, MissingPoint, PointIndex, choose_batch_count, plan_smoke
from rs_constraint_lab.v07 import POSITIVE_GRID
from rs_constraint_lab.workstore import Layout


def test_batch_count_respects_the_45_second_target_and_the_slow_item_floor():
    assert choose_batch_count([]) == 1
    assert choose_batch_count([61.0]) == 1
    assert choose_batch_count([0.5, 0.5, 0.5]) == 90
    assert choose_batch_count([0.3]) == 150


def test_plan_smoke_is_idempotent_and_keeps_two_problems(tmp_path):
    first = plan_smoke(tmp_path)
    second = plan_smoke(tmp_path)
    assert first["problems"] == 2
    assert first["planned_new_items"] > 0
    assert second["planned_new_items"] == 0
    assert len(list((tmp_path / "items").glob("*.json"))) == 0


def test_disk_book_raises_until_a_point_is_durable(tmp_path):
    plan_smoke(tmp_path)
    layout = Layout(tmp_path)
    index = PointIndex(layout)
    index.load()
    book = DiskBook(index=index, slots=__import__("rs_constraint_lab.gen007_exec", fromlist=["_world"])._world()["slots"], alphabet="W4", rho="1")
    rule = parse_expression("dissolve(0-1) => continuous", 4, order=3)
    with pytest.raises(MissingPoint):
        book.evaluate(rule, Fraction(1))
    assert POSITIVE_GRID[0] > 0
