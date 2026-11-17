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
    def __init__():
        self.nodes: list[Expr] = []
        self.hash_table: dict[Expr, int] = {}

    def make_node(self, node: Expr) -> int:
        if node in 
