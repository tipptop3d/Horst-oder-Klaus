import math

from . import add, divide, multiply, node, number, power


class Atan(node.Node):
    """Negation Node"""

    def __init__(self, arg):
        self.arg = arg

    def copy(self):
        return Atan(self.arg.copy())

    def evaluate(self, value):
        return math.atan(self.arg.evaluate(value))

    def diff(self):
        return multiply.Multiply(
            self.arg.diff(),
            divide.Divide(
                number.Number(1),
                add.Add(
                    power.Pow(self.arg, number.Number(2)),
                    number.Number(1)
                )
            )
        )

    def simplify(self):
        self.arg = self.arg.simplify()
        return super().simplify()

    def to_infix(self):
        return 'arctan({})'.format(self.arg.to_infix())
