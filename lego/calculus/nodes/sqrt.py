import math

from . import number, power, root


class Sqrt(root.Root):
    """Negation Node"""

    def __init__(self, arg):
        self.arg = arg
    
    def copy(self):
        return Sqrt(self.arg.copy())

    def evaluate(self, value):
        return math.sqrt(value.evaluate())

    def simplify(self):
        self.arg = self.arg.simplify()

        if isinstance(self.arg, power.Pow):
            exponent = self.arg.right
            if isinstance(exponent, number.Number) and exponent.value == 2:
                return self.arg.left.simplify()
        
        if self.arg is number.Number(0):
            return number.Number(0)
        
        if self.arg is number.Number(1):
            return number.Number(1)

        return super().simplify()

    def to_infix(self):
        return 'sqrt({})'.format(self.base, self.arg.to_infix())
