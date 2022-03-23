class Node:
    """Node for the binary tree"""

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def copy(self):
        return self.__class__(self.left.copy(), self.right.copy())

    def evaluate(self, **kwargs):
        """Evaluates the result of a Expression recursively, substituting
        kwargs to variables. Trying to evaluate a Expression with undefined
        variables leads to an error. First positional argument is counted as
        x.

        Example:
        f = Expression('(y+2)*x')
        f(2, y=3) -> (3+2)*2 -> 10
        """

    def to_infix(self):
        """Converts a Expression to infix-notation, recursively."""

    def diff(self):
        "Returns a Expression Tree representing the derivative of the function"
    
    def simplify(self):
        """Tries to simplify the Expression as much as possible
        Trying to implement:
            - Calculate Explicit Numbers
            - x + 0 -> x
            - x - 0 -> x
            - 0 - x -> -x
            - x * 0 -> 0
            - x * 1 -> x
            - x / 1 -> x
            - x ^ 0 -> 1
            - x ^ 1 -> x
            - x * (y / z) -> (x * y) / z

            TODO: 
            - Simplifying Fractions
            - Unifiying same denominator / Fraction Rules
            - Power Rules
            - Extended Parenthesis Rules

            """
        return self
