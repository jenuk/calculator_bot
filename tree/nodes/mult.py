from ..node import Node, operator_dict

class MultNode(Node):
    symb = "*"
    arguments = 2
    priority = 1
    acts_as_number = False

    def apply(self):
        if self.first is None or self.last is None:
            raise MalformedExpressionException("Not enough arguments for multiplication")
        return self.first.apply() * self.last.apply()

operator_dict["*"] = MultNode