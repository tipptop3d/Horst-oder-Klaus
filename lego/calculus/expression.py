"""
Representation of a expression
Parses given tokens using an recursive descent parser respecting a grammar:

expression = factor {'+' | '-' factor};
factor = power {'*' | '/' power};
power = unary {'^' unary};
unary = ('-' | '+' | ) term;
term = '(' expression ')' | number | function | variable | constant;
number = {digit}['.' {digit}];
function = function_name '(' term ')';
digit = 0|..|9;
variable = 'a'|..|'z';
constant = 'e' | 'pi' | 'tau';
"""


from .exception import ParsingError
from .nodes import (Acos, Add, Asin, Atan, Constant, Cos, Divide, Ln, Log,
                    Multiply, Negate, Number, Pow, Root, Sin, Sqrt, Subtract,
                    Tan, Variable)

class _Token:
    """Representing a token
    """
    def __init__(self, type_, value) -> None:
        self.type_ = type_
        self.value = value


def _tokenize(token: str):
    """Converts a token string to a token"""
    type_, value = token.strip('()').split(':')
    return _Token(type_, value)


def _parse(tokens):
    """Parses a sequence of tokens in RPN-Notation
    using a stack-based algorithm.

    :param tokens: Sequence of tokens in RPN-Notation
    :type tokens: List[Token]
    :raises ParsingError: Input String was not correct
    :return: Root Node of Expression Tree
    :rtype: Node
    """
    expr_stack = []
    input_stream = [_tokenize(token) for token in tokens]

    for token in input_stream:
        if token.type_ == 'VAL':
            if token.value == 2.718281828459045:
                curr_expr = Constant('e')
            else:
                curr_expr = Number(float(token.value))

        if token.type_ == 'VAR':
            curr_expr = Variable()

        if token.type_ == 'UNMINUS':
            curr_expr = Negate(expr_stack.pop())

        if token.type_ == 'PLUS':
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Add(left, right)

        if token.type_ == 'MINUS':
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Subtract(left, right)

        if token.type_ == 'TIMES':
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Multiply(left, right)

        if token.type_ == 'DIV':
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Divide(left, right)

        if token.type_ == 'POW':
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Pow(left, right)

        if token.type_ == 'LOG':
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Log(left, right)

        if token.type_ == 'LN':
            curr_expr = Ln(expr_stack.pop())

        if token.type_ == 'SQRT':
            curr_expr = Sqrt(expr_stack.pop())

        if token.type_ == 'ROOT':
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Root(left, right)

        if token.type_ == 'SIN':
            curr_expr = Sin(expr_stack.pop())

        if token.type_ == 'ASIN':
            curr_expr = Asin(expr_stack.pop())

        if token.type_ == 'TAN':
            curr_expr = Tan(expr_stack.pop())

        if token.type_ == 'ATAN':
            curr_expr = Atan(expr_stack.pop())

        if token.type_ == 'COS':
            curr_expr = Cos(expr_stack.pop())

        if token.type_ == 'ACOS':
            curr_expr = Acos(expr_stack.pop())

        expr_stack.append(curr_expr)

    if len(expr_stack) > 1:
        raise ParsingError('The input String is not a correct expression')

    return expr_stack[-1]


class Expression:
    r"""Uses a binary tree to represent a Expression
    Example:
    Representation of: ln(4) - 3*x^3

             -
            / \
           /   \
         ln     \
         /       *
        4       / \
               3   \
                    ^
                   / \
                  x   3
    """
    def __init__(self, tokens=None, root=None):
        if tokens:
            self.tree = _parse(tokens)
        else:
            self.tree = root

    def evaluate(self, value):
        """Evaluates the Expression.

        :param value: Value for x
        :type value: int | float
        :return: result of evaluation
        :rtype: float
        """
        return self.tree.evaluate(value)

    def to_infix(self):
        """Converts the expression to infix-notation
        using a visitor pattern.

        :return: Expression in infix-notation
        :rtype: str
        """
        return self.tree.to_infix()

    __str__ = to_infix

    def diff(self, simplify=True):
        """Returns a the derivative of the Expression, respects to x

        :param simplify: Simplify the tree afterwards, defaults to True
        :type simplify: bool, optional
        :return: First derivative
        :rtype: Expression
        """
        tree = Expression(root=self.tree.diff())
        if simplify:
            tree.simplify()
        return tree

    def simplify(self):
        """Simplifies the tree in-place.
        Current Rules:
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

        :return: self, for chaining
        :rtype: Expression
        """
        self.tree = self.tree.simplify()
        return self
