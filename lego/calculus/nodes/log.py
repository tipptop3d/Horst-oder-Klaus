"""Logarithm node"""

import math

from . import divide, ln, node


class Log(node.Node):
    """Logarithm node"""

    def __init__(self, base, arg):
        self.base = base
        self.arg = arg

    def natural_log(self):
        """Returns the natural logarithm version of any
        logarithm

        :return: Natural Logarithm
        :rtype: Node
        """
        return divide.Divide(ln.Ln(self.arg), ln.Ln(self.base))

    def copy(self):
        return Log(self.arg.copy(), self.base.copy())

    def evaluate(self, value):
        return math.log(self.arg.evaluate(value), self.base.evaluate(value))

    def diff(self):
        return self.natural_log().diff()

    def simplify(self):
        self.base = self.base.simplify()
        self.arg = self.arg.simplify()

        return super().simplify()

    def to_infix(self):
        return 'log_{}({})'.format(self.base, self.arg.to_infix())
