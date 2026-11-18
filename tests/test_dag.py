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


def test_constant_folding():
    arena = DagArena()
    x = arena.make_node(Num(3))
    y = arena.make_node(Num(9))
    first = arena.make_node(Mul(x, y))
    second = arena.make_node(Add(x, y))
    third = arena.make_node(Div(y, x))
    fourth = arena.make_node(Sub(y, x))
    fifth = arena.make_node(Exp(y, x))
    assert first == arena.make_node(Num(27))
    assert second == arena.make_node(Num(12))
    assert third == arena.make_node(Num(3))
    assert fourth == arena.make_node(Num(6))
    assert fifth == arena.make_node(Num(729))

def test_useless_expressions():
    arena = DagArena()
    x = arena.make_node(Var("x"))
    y = arena.make_node(Num(1))
    z = arena.make_node(Num(0))
    first = arena.make_node(Mul(x,y))
    second = arena.make_node(Mul(x,z))
    third = arena.make_node(Exp(x,y))
    fourth = arena.make_node(Add(x,z))
    fifth = arena.make_node(Sub(x,z))
    sixth = arena.make_node(Mul(y,x))
    seventh = arena.make_node(Exp(x,z))
    eighth = arena.make_node(Add(z,x))
    ninth = arena.make_node(Mul(z,x))
    tenth = arena.make_node(Sub(x,x))
    eleventh = arena.make_node(Div(x,y))
    assert first == x
    assert second == z
    assert third == x
    assert fourth == x
    assert fifth == x
    assert sixth == x
    assert seventh == y
    assert eighth == x
    assert ninth == z
    assert tenth == z
    assert eleventh == x