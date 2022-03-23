from . import node, number


class Negate(node.Node):
    """Negation Node"""

    def __init__(self, arg):
        self.arg = arg

    def copy(self):
        return Negate(self.arg.copy())

    def evaluate(self, value):
        return -self.arg.evaluate(value)

    def diff(self):
        return Negate(self.arg.diff())

    def simplify(self):
        self.arg = self.arg.simplify()

        if self.arg is number.Number(0):
            return number.Number(0)

        if isinstance(self.arg, Negate):
            return self.arg.arg.simplify()

        return super().simplify()

    def to_infix(self):
        return '(-{})'.format(self.arg.to_infix())
