"""Variable node"""

from . import node, number


class Variable(node.Node):
    """Variable node. Represents x in an Expression"""

    def copy(self):
        return Variable()

    def evaluate(self, value):
        return value

    def diff(self):
        return number.Number(1)

    def to_infix(self):
        return 'x'
