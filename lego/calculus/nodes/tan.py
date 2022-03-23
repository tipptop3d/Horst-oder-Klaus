import math

from . import cos, divide, multiply, node, number, power


class Tan(node.Node):
    """Negation Node"""

    def __init__(self, arg):
        self.arg = arg

    def copy(self):
        return Tan(self.arg.copy())

    def evaluate(self, value):
        return math.tan(self.arg.evaluate(value))

    def diff(self):
        return multiply.Multiply(
            self.arg.diff(),
            power.Pow(
                divide.Divide(
                    number.Number(1),
                    cos.Cos(self.arg)
                ),
                number.Number(2)
            )
        )

    def simplify(self):
        self.arg = self.arg.simplify()

        if self.arg is number.Number(0):
            return number.Number(0)

        return super().simplify()

    def to_infix(self):
        return '(tan({}))'.format(self.arg.to_infix())
