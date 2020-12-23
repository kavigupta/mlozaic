from abc import ABC, abstractmethod

import attr

from ..constants import MAX_SHAPES
from ..transforms import TRANSFORMS, translate, scale
from ..leaves import LEAVES
from ..value import Item
from .node import Form, Error, TooManyShapesError
from .expression import Variable


@attr.s
class Primitive(Form):
    tag = attr.ib()
    color = attr.ib()
    cx = attr.ib()
    cy = attr.ib()
    rx = attr.ib()
    ry = attr.ib()

    @classmethod
    def tags(cls):
        return list(LEAVES)

    @classmethod
    def parse(cls, tag, operands):
        return cls(tag, *operands)

    def evaluate(self, env):
        return [Item(LEAVES[self.tag], self._transform(env), self.color.evaluate(env))]

    def _transform(self, env):
        return translate(self.cx.evaluate(env), self.cy.evaluate(env)) @ scale(
            self.rx.evaluate(env), self.ry.evaluate(env)
        )

    @property
    def tree(self):
        return [
            self.tag,
            self.color.tree,
            self.cx.tree,
            self.cy.tree,
            self.rx.tree,
            self.ry.tree,
        ]


@attr.s
class Transform(Form):
    transform = attr.ib()
    operands = attr.ib()

    @classmethod
    def tags(cls):
        return list(TRANSFORMS)

    @classmethod
    def parse(cls, tag, operands):
        return cls(tag, operands)

    def evaluate(self, env):
        parameter, children = [op.evaluate(env) for op in self.operands]
        return [
            Item(
                child.type,
                TRANSFORMS[self.transform](parameter) @ child.transform,
                child.color,
            )
            for child in children
        ]

    @property
    def tree(self):
        return [self.transform] + [op.tree for op in self.operands]


@attr.s
class SimpleForm(Form):
    operands = attr.ib()

    @classmethod
    def parse(cls, tag, operands):
        return cls(operands)

    @property
    def tree(self):
        [tag] = self.tags()
        return [tag] + [op.tree for op in self.operands]


class Combine(SimpleForm):
    @classmethod
    def tags(cls):
        return ["combine"]

    def evaluate(self, env):
        a, b = [op.evaluate(env) for op in self.operands]
        return a + b


class Repeat(SimpleForm):
    @classmethod
    def tags(cls):
        return ["repeat"]

    def evaluate(self, env):
        var, start, end, body = self.operands
        start, end = start.evaluate(env), end.evaluate(env)
        shape = []
        for i in range(int(start), int(end)):
            child_env = env.copy()
            child_env[var.name] = i
            shape += body.evaluate(child_env)
            if len(shape) > MAX_SHAPES:
                raise TooManyShapesError
        return shape

    @classmethod
    def custom_sample(cls, sampler, variables, depth):
        variable = Variable.fresh_variable(variables)
        start, end = (
            sampler.sample(variables, production="N", depth=depth + 1),
            sampler.sample(variables, production="N", depth=depth + 1),
        )
        body = sampler.sample(variables | {variable}, production="D", depth=depth + 1)
        return cls.parse("repeat", (Variable.parse(variable), start, end, body))


class If(SimpleForm):
    @classmethod
    def tags(cls):
        return ["if"]

    def evaluate(self, env):
        condition, consequent = [op.evaluate(env) for op in self.operands]
        if condition:
            return consequent
        else:
            return []


class IfE(SimpleForm):
    @classmethod
    def tags(cls):
        return ["ife"]

    def evaluate(self, env):
        condition, consequent, alternative = [op.evaluate(env) for op in self.operands]
        if condition:
            return consequent
        else:
            return alternative
