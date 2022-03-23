import math

from . import multiply, negate, node, number, sin


class Cos(node.Node):
    """Negation Node"""

    def __init__(self, arg):
        self.arg = arg

    def copy(self):
        return Cos(self.arg.copy())

    def evaluate(self, value):
        return math.cos(self.arg.evaluate(value))

    def diff(self):
        return multiply.Multiply(self.arg.diff(), negate.Negate(sin.Sin(self.arg)))

    def simplify(self):
        self.arg = self.arg.simplify()

        if self.arg is number.Number(0):
            return number.Number(1)

        return super().simplify()

    def to_infix(self):
        return 'cos({})'.format(self.arg.to_infix())
