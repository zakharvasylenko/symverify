from symverify.core_ir.lexer import Token, TokenType
from dataclasses import dataclass
from enum import Enum, auto

class TrigFunc(Enum):
    SIN = auto()
    COS = auto()
    TAN = auto()

@dataclass(frozen=True)
class Trig:
    type: TrigFunc
    content: Expr

@dataclass(frozen=True)
class Num:
    content: int | float

@dataclass(frozen=True)
class Var:
    content: str
    def __post_init__(self):
        if len(self.content) != 1:
            raise SyntaxError

@dataclass(frozen=True)
class Add:
    left: Expr
    right: Expr

@dataclass(frozen=True)
class Sub:
    left: Expr
    right: Expr

@dataclass(frozen=True)
class Mul:
    left: Expr
    right: Expr

@dataclass(frozen=True)
class Div:
    left: Expr
    right: Expr


@dataclass(frozen=True)
class Exp:
    left: Expr
    right: Expr

Expr = Num | Var | Add | Sub | Mul | Div | Exp | Trig

TRIG_FUNCS = {"sin": TrigFunc.SIN,
              "cos": TrigFunc.COS,
              "tan": TrigFunc.TAN}

INFIX_NODES = {TokenType.ADD: Add,
               TokenType.SUB: Sub,
               TokenType.MUL: Mul,
               TokenType.DIV: Div,
               TokenType.EXP: Exp}

BINDING_POWERS = {Add: 10,
                  Sub: 10,
                  Div: 20,
                  Mul: 20,
                  Exp: 30}

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self): # see without advancing pos
        if (self.pos < len(self.tokens)):
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

    def parse_expr(self, min_bp: int = 0) -> Expr:
        token = self.consume()
        if token.kind == TokenType.NUM:
            lhs = Num(token.content)
        elif token.kind == TokenType.IDENT:
            if token.content in TRIG_FUNCS:
                if (self.consume().kind != TokenType.LPAREN):
                    raise SyntaxError
                inner = self.parse_expr()
                if self.consume().kind != TokenType.RPAREN:
                    raise SyntaxError
                lhs = Trig(TRIG_FUNCS[token.content], inner)
            elif isinstance(token.content, str) and len(token.content) == 1:
                lhs = Var(token.content)
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
            lhs = node_cls(lhs, rhs)
        return lhs
            






