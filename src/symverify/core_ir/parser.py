from __future__ import annotations
from symverify.core_ir.lexer import Token, TokenType
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

TRIG_FUNCS = {
    "sin": TrigFunc.SIN,
    "cos": TrigFunc.COS,
    "tan": TrigFunc.TAN,
}

INFIX_NODES = {
    TokenType.ADD: Add,
    TokenType.SUB: Sub,
    TokenType.MUL: Mul,
    TokenType.DIV: Div,
    TokenType.EXP: Exp,
}

BINDING_POWERS = {
    Add: 10,
    Sub: 10,
    Div: 20,
    Mul: 20,
    Exp: 30,
}


class Parser:
    def __init__(self, tokens: list[Token], arena: DagArena | None = None):
        self.tokens = tokens
        self.pos = 0
        self.arena = arena if arena is not None else DagArena()

    def peek(self):  # see without advancing pos
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            return None

    def consume(self):
        token = self.peek()
        if token is None:
            raise SyntaxError
        else:
            self.pos += 1
            return token

    def parse_expr(self, min_bp: int = 0) -> int:
        token = self.consume()
        if token.kind == TokenType.NUM:
            lhs = self.arena.make_node(Num(token.content))
        elif token.kind == TokenType.IDENT:
            if token.content in TRIG_FUNCS:
                if self.consume().kind != TokenType.LPAREN:
                    raise SyntaxError
                inner = self.parse_expr()
                if self.consume().kind != TokenType.RPAREN:
                    raise SyntaxError
                lhs = self.arena.make_node(Trig(TRIG_FUNCS[token.content], inner))
            elif isinstance(token.content, str) and len(token.content) == 1:
                lhs = self.arena.make_node(Var(token.content))
            else:
                raise SyntaxError
        elif token.kind == TokenType.LPAREN:
            lhs = self.parse_expr()
            if self.consume().kind != TokenType.RPAREN:
                raise SyntaxError
        else:
            raise SyntaxError
        while True:
            op_token = self.peek()
            if op_token is None or op_token.kind not in INFIX_NODES:
                break
            node_cls = INFIX_NODES[op_token.kind]
            bp = BINDING_POWERS[node_cls]
            if bp < min_bp:
                break
            self.consume()
            if node_cls == Exp:
                next_min_bp = bp - 1
            else:
                next_min_bp = bp + 1
            rhs = self.parse_expr(next_min_bp)
            lhs = self.arena.make_node(node_cls(lhs, rhs))
        return lhs