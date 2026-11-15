import pytest
from symverify.core_ir.lexer import Token, TokenType
from symverify.core_ir.parser import parse, Num, Var, Add, Mul, Sub, Div, Exp, Trig, TrigFunc


def test_basic_tokens(): #27 + x - 5
    tokens = [
        Token(TokenType.NUM, 27),
        Token(TokenType.ADD),
        Token(TokenType.IDENT, "x"),
        Token(TokenType.SUB),
        Token(TokenType.NUM, 5),
        Token(TokenType.EOF)
    ] 
    parsed = parse(tokens)
    assert parsed == Sub(Add(Num(27), Var("x")), Num(5))

def test_medium_expression(): # (2 * 3) / 4 ^ 5
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
        Token(TokenType.EOF)
    ]
    parsed = parse(tokens)
    assert parsed == Div(Mul(Num(2),Num(3)), Exp(Num(4), Num(5)))

def test_complicated_expression(): # 3.14 * sin(x)
    tokens = [
        Token(TokenType.NUM, 3.14),
        Token(TokenType.MUL),
        Token(TokenType.IDENT, "sin"),
        Token(TokenType.LPAREN),
        Token(TokenType.IDENT, "x"),
        Token(TokenType.RPAREN),
        Token(TokenType.EOF)  
    ]
    parsed = parse(tokens)
    assert parsed == Mul(Num(3.14), Trig(TrigFunc.SIN, Var("x")))

