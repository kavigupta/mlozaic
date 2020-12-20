from abc import ABC, abstractmethod

import attr


class Node(ABC):
    @classmethod
    @abstractmethod
    def tags(cls):
        pass

    @abstractmethod
    def evaluate(self, env):
        pass

    @classmethod
    def custom_sample(cls, sampler, variables):
        pass

    @property
    @abstractmethod
    def tree(self):
        pass

    @property
    def code(self):
        from ..parser import flatten

        return flatten(self.tree)


class Atom(Node):
    @classmethod
    @abstractmethod
    def parse(cls, s):
        pass


class Form(Node):
    @classmethod
    @abstractmethod
    def parse(cls, tag, operands):
        pass


@attr.s
class Error(Node):
    @classmethod
    def tags(cls):
        raise SyntaxError("error in parsing")

    def evaluate(self, env):
        raise SyntaxError("error in parsing")

    @property
    def tree(self):
        return "#err"
