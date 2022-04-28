"""Constant node"""

import math

from ..exception import UnknownConstant
from . import node, number


class Constant(node.Node):
    """Constant node. Multiton. Looks up the math module"""

    _instances = dict()

    def __new__(cls, name):
        if name in cls._instances:
            return cls._instances[name]

        obj = super(Constant, cls).__new__(cls)
        cls._instances[name] = obj
        return obj

    def __init__(self, name):
        self.name = name

    def copy(self):
        return Constant(self.name)

    def evaluate(self, _):
        if self.name == 'e':
            return math.e
        if self.name == 'pi':
            return math.pi
        else:
            raise UnknownConstant('Constant {} is unknown'.format(self.name))

    def diff(self):
        return number.Number(0)

    def to_infix(self):
        return self.name
