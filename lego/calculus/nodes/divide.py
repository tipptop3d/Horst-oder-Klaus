from . import multiply, node, number, power, subtract


class Divide(node.Node):
    """Division Node"""

    def evaluate(self, value):
        return self.left.evaluate(value) / self.right.evaluate(value)

    def diff(self):
        return Divide(
            subtract.Subtract(
                multiply.Multiply(self.left.diff(), self.right.copy()),
                multiply.Multiply(self.left.copy(), self.right.diff())
            ),
            power.Pow(self.right, number.Number(2))
        )

    def simplify(self):
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        if self.left is number.Number(0):
            return number.Number(0)
        if self.right is number.Number(0):
            raise ZeroDivisionError
        if isinstance(self.left, number.Number) and isinstance(self.right, number.Number):
            if (self.left.value / self.right.value).is_integer():
                return number.Number(self.left.value / self.right.value)

        return super().simplify()

    def to_infix(self):
        return '({} / {})'.format(self.left.to_infix(), self.right.to_infix())
