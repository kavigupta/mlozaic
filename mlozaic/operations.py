from operator import add, sub, mul, truediv, mod, lt, le, gt, ge, eq, and_, or_, not_

NUM_OPS = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
    "%": mod,
}

COMPARISONS = {
    "<": lt,
    "<=": le,
    ">": gt,
    ">=": ge,
    "=": eq,
}

BOOL_BINARY_OPS = {"and": and_, "or": or_}
BOOL_UNARY_OP = {"~": not_}

OPERATIONS = {**NUM_OPS, **COMPARISONS, **BOOL_BINARY_OPS, **BOOL_UNARY_OP}
