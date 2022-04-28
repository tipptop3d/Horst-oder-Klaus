"""Add node"""

from . import node, number


class Add(node.Node):
    """Add node"""

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    
    def copy(self):
        return Add(self.left.copy(), self.right.copy())

    def evaluate(self, value):
        return self.left.evaluate(value) + self.right.evaluate(value)

    def diff(self):
        return Add(self.left.diff(), self.right.diff())

    def simplify(self):
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        if self.left is number.Number(0):
            return self.right
        if self.right is number.Number(0):
            return self.left
        if isinstance(self.left, number.Number) and isinstance(self.right, number.Number):
            return number.Number(self.left.value + self.right.value)

        return super().simplify()

    def to_infix(self):
        return '({} + {})'.format(self.left.to_infix(), self.right.to_infix())
