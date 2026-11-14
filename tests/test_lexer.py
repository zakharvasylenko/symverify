from symverify.core_ir.lexer import tokenize, Token, TokenType
import pytest

def test_basic_expression():
    tokens = tokenize("27 + x - 5")
    assert tokens == [Token(TokenType.NUM, 27),
                      Token(TokenType.ADD),
                      Token(TokenType.IDENT, "x"),
                      Token(TokenType.SUB),
                      Token(TokenType.NUM, 5),
                      Token(TokenType.EOF)]

def test_more_basic_expression():
    tokens = tokenize("12 - 10 - 1")
    assert tokens == [Token(TokenType.NUM, 12),
                      Token(TokenType.SUB), 
                      Token(TokenType.NUM, 10),
                      Token(TokenType.SUB),
                      Token(TokenType.NUM, 1),
                      Token(TokenType.EOF)]

def test_medium_expression():
    tokens = tokenize("(2 * 3) / 4 ^ 5")
    assert tokens == [Token(TokenType.LPAREN),
                      Token(TokenType.NUM, 2),
                      Token(TokenType.MUL),
                      Token(TokenType.NUM, 3),
                      Token(TokenType.RPAREN),
                      Token(TokenType.DIV),
                      Token(TokenType.NUM, 4),
                      Token(TokenType.EXP),
                      Token(TokenType.NUM, 5),
                      Token(TokenType.EOF)]

def test_complicated_expression():
    tokens = tokenize("3.14 * sin(x)")
    assert tokens == [Token(TokenType.NUM, 3.14),
                      Token(TokenType.MUL),
                      Token(TokenType.IDENT, "sin"),
                      Token(TokenType.LPAREN),
                      Token(TokenType.IDENT, "x"),
                      Token(TokenType.RPAREN),
                      Token(TokenType.EOF)]

def test_invalid_character():
    with pytest.raises(SyntaxError):
        tokenize("3 $$$$ 6 @ 8")



