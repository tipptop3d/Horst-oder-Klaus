from . import divide, node, number, power


class Root(node.Node):
    """Negation Node"""

    def __init__(self, n, arg):
        self.n = n
        self.arg = arg
    
    def power(self):
        return power.Pow(self.arg, divide.Divide(number.Number(1), self.n))

    def copy(self):
        return Root(self.arg.copy())

    def evaluate(self, value):
        return self.power().evaluate(value)

    def diff(self):
        return self.power().diff()

    def simplify(self):
        self.arg = self.arg.simplify()

        return super().simplify()

    def to_infix(self):
        return 'nrt({},{})'.format(self.base, self.arg.to_infix())
