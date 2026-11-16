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
