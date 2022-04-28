"""Number node. Multiton"""

from . import node


class Number(node.Node):
    """Number node. Multiton"""

    _instances = dict()

    def __new__(cls, value):
        if value in cls._instances:
            return cls._instances[value]
        else:
            obj = super(Number, cls).__new__(cls)
            cls._instances[value] = obj
            return obj

    def __init__(self, value):
        self.value = value

    def copy(self):
        return Number(self.value)

    def evaluate(self, _):
        return self.value

    def diff(self):
        return Number(0)

    def to_infix(self):
        return str(self.value)
