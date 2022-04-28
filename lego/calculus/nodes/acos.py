"""Acos node"""
import math

from calculus.nodes import negate

from . import divide, multiply, node, number, power, sqrt, subtract


class Acos(node.Node):
    """Acos node"""

    def __init__(self, arg):
        self.arg = arg

    def copy(self):
        return Acos(self.arg.copy())

    def evaluate(self, value):
        return math.acos(self.arg.evaluate(value))

    def diff(self):
        return multiply.Multiply(
            self.arg.diff(),
            negate.Negate(
                divide.Divide(
                    number.Number(1),
                    sqrt.Sqrt(
                        subtract.Subtract(
                            number.Number(1),
                            power.Pow(self.arg, number.Number(2))
                        )
                    )
                )
            )
        )

    def simplify(self):
        self.arg = self.arg.simplify()
        return super().simplify()

    def to_infix(self):
        return 'arccos({})'.format(self.arg.to_infix())
