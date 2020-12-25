from .ast.expression import (
    Constant,
    Variable,
    Color,
    NumericOperation,
    Comparison,
    BooleanBinaryOp,
    BooleanUnaryOp,
)

from .ast.drawing import (
    Primitive,
    Transform,
    Combine,
    Repeat,
    If,
    IfE,
)

grammar = {
    "N": [Constant, Variable, [NumericOperation, "N", "N"]],
    "C": [
        [Comparison, "N", "N"],
        [BooleanBinaryOp, "C", "C"],
        [BooleanUnaryOp, "C"],
    ],
    "D": [
        [Primitive, Color, "N", "N", "N", "N"],
        [Transform, "N", "D"],
        [Combine, "D", "D"],
        [Repeat, Variable, "N", "N", "D"],
        [If, "C", "D"],
        [IfE, "C", "D", "D"],
    ],
}


def alphabet(g):
    if isinstance(g, dict):
        for v in g.values():
            yield from alphabet(v)
    elif isinstance(g, list):
        for v in g:
            yield from alphabet(v)
    elif isinstance(g, str):
        return
    else:
        yield from g.tags()


ALPHABET = sorted(set(alphabet(grammar)) | set("()"))
BACKWARDS_ALPHABET = {sym: i for i, sym in enumerate(ALPHABET)}
