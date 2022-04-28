"""Multiplication node"""

from . import add, divide, node, number


class Multiply(node.Node):
    """Multiplication node"""

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def copy(self):
        return Multiply(self.left.copy(), self.right.copy())

    def evaluate(self, value):
        return self.left.evaluate(value) * self.right.evaluate(value)

    def diff(self):
        return add.Add(
            Multiply(self.left.diff(), self.right.copy()),
            Multiply(self.left.copy(), self.right.diff())
        )

    def simplify(self):
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        if self.left is number.Number(0) or self.right is number.Number(0):
            return number.Number(0)

        if self.left is number.Number(1):
            return self.right
        if self.right is number.Number(1):
            return self.left

        if isinstance(self.left, divide.Divide):
            return divide.Divide(
                Multiply(self.left.left, self.right),
                self.left.right
            ).simplify()
        if isinstance(self.right, divide.Divide):
            return divide.Divide(
                Multiply(self.right.left, self.left),
                self.right.right
            ).simplify()

        if isinstance(self.left, number.Number) and isinstance(self.right, number.Number):
            return number.Number(self.left.value * self.right.value)

        return super().simplify()

    def to_infix(self):
        return '({} * {})'.format(self.left.to_infix(), self.right.to_infix())
