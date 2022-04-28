"""natural logarithm node"""

import math

from . import divide, node, number


class Ln(node.Node):
    """natural logarithm node"""

    def __init__(self, arg):
        self.arg = arg

    def copy(self):
        return Ln(self.arg.copy())

    def evaluate(self, value):
        return math.log(self.arg.evaluate(value))

    def diff(self):
        return divide.Divide(self.arg.diff(), self.arg)

    def simplify(self):
        self.arg = self.arg.simplify()

        if self.arg is number.Number(1):
            return number.Number(0)

        return super().simplify()

    def to_infix(self):
        return 'ln({})'.format(self.arg.to_infix())
