class ParsingError(Exception):
    """Exception raised by a parsing error."""


class EvaluationError(Exception):
    """Exception raised if a Expression couldn't be evaluated."""


class DifferentationError(Exception):
    """Exception raised if a Expression couldn't be differentiated"""


class TokenizingError(Exception):
    """Raises if an error occurs while parsing"""

class UnknownConstant(Exception):
    """Raises if an unknown constant is evaluated"""
