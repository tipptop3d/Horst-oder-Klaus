"""node"""


class Node:
    """Abstract base class Node for the binary tree."""

    def copy(self):
        """Returns a deep copy of a node

        :return: Copied node
        :rtype: Node
        """

    def evaluate(self, value) -> float:
        """Evaluates the result of a Expression recursively, substituting
        x with value.

        :param value: value for x
        :type value: int | float
        :return: Result of calculation
        :rtype: float
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
