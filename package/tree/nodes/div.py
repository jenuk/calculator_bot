from ..node import Node, operator_dict
from .number import NumberNode

class DivNode(Node):
    symb = "/"
    arguments = 2
    priority = 1
    acts_as_number = False

    def apply(self):
        if self.first is None or self.last is None:
            raise MalformedExpressionException("Not enough arguments for division")
        return self.first.apply() / self.last.apply()

    def simplify(self):
        super().simplify()
        if type(self.first) == NumberNode and type(self.last) == NumberNode:
            return NumberNode(self.first.value/self.last.value)

operator_dict["/"] = DivNode