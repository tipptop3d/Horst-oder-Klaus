import math

from . import cos, multiply, node, number


class Sin(node.Node):
    """Negation Node"""

    def __init__(self, arg):
        self.arg = arg

    def copy(self):
        return Sin(self.arg.copy())

    def evaluate(self, value):
        return math.sin(self.arg.evaluate(value))

    def diff(self):
        return multiply.Multiply(self.arg.diff(), cos.Cos(self.arg))

    def simplify(self):
        self.arg = self.arg.simplify()

        if self.arg is number.Number(0):
            return number.Number(0)

        return super().simplify()

    def to_infix(self):
        return 'sin({})'.format(self.arg.to_infix())
