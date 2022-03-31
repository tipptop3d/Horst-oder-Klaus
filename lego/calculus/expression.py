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


class TokenType:
    VAL = 'VAL'
    VAR = 'VAR'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    TIMES = 'TIMES'
    DIV = 'DIV'
    POW = 'POW'
    UNMINUS = 'UNMINUS'

    SIN = 'SIN'
    ASIN = 'ASIN'
    COS = 'COS'
    ACOS = 'ACOS'
    TAN = 'TAN'
    ATAN = 'ATAN'

    ROOT = 'ROOT'
    SQRT = 'SQRT'

    LN = 'LN'
    LOG = 'LOG'


TYPE_PATTERN = {
    'VAL': TokenType.VAL,
    'VAR': TokenType.VAR,
    'PLUS': TokenType.PLUS,
    'MINUS': TokenType.MINUS,
    'TIMES': TokenType.TIMES,
    'DIV': TokenType.DIV,
    'POW': TokenType.POW,
    'UNMINUS': TokenType.UNMINUS,

    'SIN': TokenType.SIN,
    'ASIN': TokenType.ASIN,
    'COS': TokenType.COS,
    'ACOS': TokenType.ACOS,
    'TAN': TokenType.TAN,
    'ATAN': TokenType.ATAN,

    'ROOT': TokenType.ROOT,
    'SQRT': TokenType.SQRT,

    'LN': TokenType.LN,
    'LOG': TokenType.LOG,
}


class _Token:
    def __init__(self, _type, value) -> None:
        self._type = _type
        self.value = value


def _tokenize(token: str):
    _type, value = token.strip('()').split(':')
    return _Token(TYPE_PATTERN[_type], value)


def _parse(tokens):
    expr_stack = []
    input_stream = [_tokenize(token) for token in tokens]

    for token in input_stream:
        if token._type == TokenType.VAL:
            if token.value == 2.718281828459045:
                curr_expr = Constant('e')
            else:
                curr_expr = Number(float(token.value))

        if token._type == TokenType.VAR:
            curr_expr = Variable()

        if token._type == TokenType.UNMINUS:
            curr_expr = Negate(expr_stack.pop())

        if token._type == TokenType.PLUS:
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Add(left, right)

        if token._type == TokenType.MINUS:
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Subtract(left, right)

        if token._type == TokenType.TIMES:
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Multiply(left, right)

        if token._type == TokenType.DIV:
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Divide(left, right)

        if token._type == TokenType.POW:
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Pow(left, right)

        if token._type == TokenType.LOG:
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Log(left, right)

        if token._type == TokenType.LN:
            curr_expr = Ln(expr_stack.pop())

        if token._type == TokenType.SQRT:
            curr_expr = Sqrt(expr_stack.pop())

        if token._type == TokenType.ROOT:
            right = expr_stack.pop()
            left = expr_stack.pop()
            curr_expr = Root(left, right)

        if token._type == TokenType.SIN:
            curr_expr = Sin(expr_stack.pop())

        if token._type == TokenType.ASIN:
            curr_expr = Asin(expr_stack.pop())

        if token._type == TokenType.TAN:
            curr_expr = Tan(expr_stack.pop())

        if token._type == TokenType.ATAN:
            curr_expr = Atan(expr_stack.pop())

        if token._type == TokenType.COS:
            curr_expr = Cos(expr_stack.pop())

        if token._type == TokenType.ACOS:
            curr_expr = Acos(expr_stack.pop())

        expr_stack.append(curr_expr)

    if len(expr_stack) > 1:
        raise ParsingError('The input String is not a correct expression')

    return expr_stack[-1]


class Expression:
    r"""
    Uses a binary tree to represent a Expression
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
        """Evaluates the Expression. Variables can be substituted by arguments.
        If more than one variable is present, keyword arguments are needed.
        All variables have to be substituted. Excess Variables are ignored

        Examples:
        >>> f = Expression('2x+5')
        >>> f(2)
        9
        >>> f(x=2, z=4)
        9
        >>> f(y=2)
        EvaluationError('Cannot evaluate undefined variable')
        >>> f = Expression('x+y')
        >>> f(2)
        EvaluationError('Unspecified variable')
        """
        return self.tree.evaluate(value)

    def to_infix(self):
        return self.tree.to_infix()

    __str__ = to_infix

    def diff(self, simplify=True):
        """Returns a the derivative of the Expression, respect to x"""
        tree = Expression(root=self.tree.diff())
        if simplify:
            tree.simplify()
        return tree

    def simplify(self):
        self.tree = self.tree.simplify()
        return self
