"""Root node"""

from . import divide, node, number, power


class Root(node.Node):
    """Root node"""

    def __init__(self, degree, radicand):
        self.degree = degree
        self.radicand = radicand

    def power(self):
        """Returns a representation of a root as a power

        :return: Power Representation
        :rtype: Node
        """
        return power.Pow(self.radicand, divide.Divide(number.Number(1), self.degree))

    def copy(self):
        return Root(self.degree.copy(), self.radicand.copy())

    def evaluate(self, value):
        return self.power().evaluate(value)

    def diff(self):
        return self.power().diff()

    def simplify(self):
        self.radicand = self.radicand.simplify()
        return super().simplify()

    def to_infix(self):
        return 'nrt({},{})'.format(self.degree.to_infix(), self.radicand.to_infix())
