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
