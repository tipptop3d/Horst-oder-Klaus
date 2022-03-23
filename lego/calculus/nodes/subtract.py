from . import negate, node, number


class Subtract(node.Node):
    """Subtract Node"""

    def evaluate(self, value):
        return self.left.evaluate(value) - self.right.evaluate(value)

    def diff(self):
        return Subtract(self.left.diff(), self.right.diff())
    
    def simplify(self):
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        if self.left is number.Number(0):
            return negate.Negate(self.right)
        if self.right is number.Number(0):
            return self.left
        if isinstance(self.left, number.Number) and isinstance(self.right, number.Number):
            return number.Number(self.left.value - self.right.value)
        
        return super().simplify()

    def to_infix(self):
        return '({} - {})'.format(self.left.to_infix(), self.right.to_infix())
