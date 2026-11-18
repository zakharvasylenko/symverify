from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto 


class TrigFunc(Enum):
    SIN = auto()
    COS = auto()
    TAN = auto()

@dataclass(frozen=True)
class Trig:
    type: TrigFunc
    content: int

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
    left: int
    right: int

@dataclass(frozen=True)
class Sub:
    left: int
    right: int

@dataclass(frozen=True)
class Mul:
    left: int
    right: int

@dataclass(frozen=True)
class Div:
    left: int
    right: int


@dataclass(frozen=True)
class Exp:
    left: Expr
    right: Expr

Expr = Num | Var | Add | Sub | Mul | Div | Exp | Trig

class DagArena:
    def __init__(self):
        self.nodes: list[Expr] = []
        self.hash_table: dict[Expr, int] = {}

    def make_node(self, node: Expr) -> int:
        if isinstance(node, Add | Sub | Mul | Div | Exp):
            l = self.nodes[node.left]
            r = self.nodes[node.right]
            if isinstance(l, Num) and isinstance(r, Num):
                match node:
                    case Add():
                        return self.make_node(Num(l.content + r.content))
                    case Sub():
                        return self.make_node(Num(l.content - r.content))
                    case Mul():
                        return self.make_node(Num(l.content * r.content))
                    case Div() if r.content != 0:
                        return self.make_node(Num(l.content / r.content))
                    case Exp():
                        return self.make_node(Num(l.content ** r.content))
        if node in self.hash_table:
            return self.hash_table[node]
        else:
            self.nodes.append(node)
            new_len = len(self.hash_table)
            self.hash_table[node] = new_len
            return new_len
            
