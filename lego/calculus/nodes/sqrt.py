"""Sqrt node"""

import math

from . import node, number, power


class Sqrt(node.Node):
    """Sqrt node. Simpler version of root for degree=2"""

    def __init__(self, radicand):
        self.radicand = radicand

    def copy(self):
        return Sqrt(self.radicand.copy())

    def evaluate(self, value):
        return math.sqrt(value.evaluate())

    def simplify(self):
        self.radicand = self.radicand.simplify()

        if isinstance(self.radicand, power.Pow):
            exponent = self.radicand.right
            if isinstance(exponent, number.Number) and exponent.value == 2:
                return self.radicand.left.simplify()

        if self.radicand is number.Number(0):
            return number.Number(0)

        if self.radicand is number.Number(1):
            return number.Number(1)

        return super().simplify()

    def to_infix(self):
        return 'sqrt({})'.format(self.radicand.to_infix())
