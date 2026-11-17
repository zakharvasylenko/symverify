import pytest
from symverify.core_ir.ast import DagArena, Num, Var, Add, Sub, Mul, Div, Exp, Trig, TrigFunc

def test_basic_dag():
    arena = DagArena()
    x = arena.make_node(Var("x"))
    two = arena.make_node(Num(2))
    first = arena.make_node(Exp(x, two))
    second = arena.make_node(Exp(x, two))

    assert first == second
    assert len(arena.nodes) == 3