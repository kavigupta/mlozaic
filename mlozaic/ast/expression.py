from abc import ABC, abstractmethod
from itertools import count

import attr

from .node import Atom, Form, Error
from ..constants import NUM_VARS, CONSTANTS
from ..operations import NUM_OPS, BOOL_BINARY_OPS, BOOL_UNARY_OP, COMPARISONS
from ..colors import COLORS


@attr.s
class Constant(Atom):
    value = attr.ib()

    @classmethod
    def tags(cls):
        return [str(i) for i in CONSTANTS]

    @classmethod
    def parse(cls, s):
        try:
            return cls(int(s))
        except (ValueError, TypeError):
            return Error()

    def evaluate(self, env):
        return self.value

    @property
    def tree(self):
        return str(self.value)


@attr.s
class Color(Atom):
    tag = attr.ib()

    @classmethod
    def tags(cls):
        return list(COLORS)

    @classmethod
    def parse(cls, s):
        if s in COLORS:
            return cls(s)
        return Error()

    def evaluate(self, env):
        return COLORS[self.tag]

    @property
    def tree(self):
        return self.tag


@attr.s
class Variable(Atom):
    name = attr.ib()

    @classmethod
    def tags(cls):
        return [f"${i}" for i in range(NUM_VARS)]

    @classmethod
    def parse(cls, s):
        if not isinstance(s, str) or not s.startswith("$"):
            return Error()
        return cls(s)

    @classmethod
    def fresh_variable(cls, variables):
        for i in count():
            var_name = f"${i}"
            if var_name not in variables:
                return var_name

    def evaluate(self, env):
        return env[self.name]

    @property
    def tree(self):
        return self.name


@attr.s
class Operation(Form):
    operation = attr.ib()
    operands = attr.ib()

    @classmethod
    def tags(cls):
        return list(cls.operations())

    @classmethod
    def parse(cls, tag, operands):
        return cls(tag, operands)

    @classmethod
    @abstractmethod
    def operations(cls):
        pass

    def evaluate(self, env):
        return self.operations()[self.operation](
            *[op.evaluate(env) for op in self.operands]
        )

    @property
    def tree(self):
        return [self.operation] + [op.tree for op in self.operands]


class NumericOperation(Operation):
    @classmethod
    def operations(cls):
        return NUM_OPS


class Comparison(Operation):
    @classmethod
    def operations(cls):
        return COMPARISONS


class BooleanBinaryOp(Operation):
    @classmethod
    def operations(cls):
        return BOOL_BINARY_OPS


class BooleanUnaryOp(Operation):
    @classmethod
    def operations(cls):
        return BOOL_UNARY_OP
