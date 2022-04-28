"""Power node"""

from . import constant, ln, multiply, node, number, variable


class Pow(node.Node):
    """Power node"""

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def copy(self):
        return Pow(self.left.copy(), self.right.copy())

    def evaluate(self, value):
        return self.left.evaluate(value) ** self.right.evaluate(value)

    def diff(self):
        if isinstance(self.left, variable.Variable) and isinstance(self.right, number.Number):
            return multiply.Multiply(
                self.right.copy(),
                Pow(
                    self.left.copy(),
                    number.Number(self.right.value - 1)
                )
            )

        if self.left is constant.Constant('e'):
            return multiply.Multiply(
                self.right.diff(),
                self.copy()
            )

        return multiply.Multiply(
            self.copy(),
            multiply.Multiply(
                ln.Ln(self.left.copy()),
                self.right.copy()
            ).diff()
        )

    def simplify(self):
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        if self.right is number.Number(0):
            return number.Number(1)
        if self.left is number.Number(0):
            return number.Number(0)

        if self.right is number.Number(1):
            return self.left

        if isinstance(self.left, number.Number) and isinstance(self.right, number.Number):
            return number.Number(self.left.value ** self.right.value)

        return super().simplify()

    def to_infix(self):
        return '({} ^ {})'.format(self.left.to_infix(), self.right.to_infix())
