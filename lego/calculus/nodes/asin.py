import math

from . import divide, multiply, node, number, power, sqrt, subtract


class Asin(node.Node):
    """Negation Node"""

    def __init__(self, arg):
        self.arg = arg

    def copy(self):
        return Asin(self.arg.copy())

    def evaluate(self, value):
        return math.asin(self.arg.evaluate(value))

    def diff(self):
        return multiply.Multiply(
            self.arg.diff(),
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

    def simplify(self):
        self.arg = self.arg.simplify()
        return super().simplify()

    def to_infix(self):
        return 'arcsin({})'.format(self.arg.to_infix())
