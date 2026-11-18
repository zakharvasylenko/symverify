import pytest
from symverify.core_ir.ast import (
    Add,
    DagArena,
    Div,
    Exp,
    Mul,
    Num,
    Sub,
    Trig,
    TrigFunc,
    Var,
)
from symverify.core_ir.lexer import Token, TokenType
from symverify.core_ir.parser import Parser


def test_basic_tokens():  # 27 + x - 5
    tokens = [
        Token(TokenType.NUM, 27),
        Token(TokenType.ADD),
        Token(TokenType.IDENT, "x"),
        Token(TokenType.SUB),
        Token(TokenType.NUM, 5),
        Token(TokenType.EOF),
    ]
    arena = DagArena()
    parsed = Parser(tokens, arena).parse_expr()
    expected = arena.make_node(
        Sub(
            arena.make_node(Add(arena.make_node(Num(27)), arena.make_node(Var("x")))),
            arena.make_node(Num(5)),
        )
    )
    assert parsed == expected


def test_medium_expression():  # (2 * 3) / 4 ^ 5 -> constant-folds to 6 / 1024 = 0.005859375
    tokens = [
        Token(TokenType.LPAREN),
        Token(TokenType.NUM, 2),
        Token(TokenType.MUL),
        Token(TokenType.NUM, 3),
        Token(TokenType.RPAREN),
        Token(TokenType.DIV),
        Token(TokenType.NUM, 4),
        Token(TokenType.EXP),
        Token(TokenType.NUM, 5),
        Token(TokenType.EOF),
    ]
    arena = DagArena()
    parsed = Parser(tokens, arena).parse_expr()
    expected = arena.make_node(
        Div(
            arena.make_node(Mul(arena.make_node(Num(2)), arena.make_node(Num(3)))),
            arena.make_node(Exp(arena.make_node(Num(4)), arena.make_node(Num(5)))),
        )
    )
    assert parsed == expected
    assert arena.nodes[parsed] == Num(6 / 1024)


def test_complicated_expression():  # 3.14 * sin(x)
    tokens = [
        Token(TokenType.NUM, 3.14),
        Token(TokenType.MUL),
        Token(TokenType.IDENT, "sin"),
        Token(TokenType.LPAREN),
        Token(TokenType.IDENT, "x"),
        Token(TokenType.RPAREN),
        Token(TokenType.EOF),
    ]
    arena = DagArena()
    parsed = Parser(tokens, arena).parse_expr()
    expected = arena.make_node(
        Mul(
            arena.make_node(Num(3.14)),
            arena.make_node(Trig(TrigFunc.SIN, arena.make_node(Var("x")))),
        )
    )
    assert parsed == expected