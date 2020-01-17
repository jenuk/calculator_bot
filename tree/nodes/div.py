from ..node import Node, operator_dict

class DivNode(Node):
    symb = "/"
    arguments = 2
    priority = 1
    acts_as_number = False

    def apply(self):
        if self.first is None or self.last is None:
            raise MalformedExpressionException("Not enough arguments for division")
        return self.first.apply() / self.last.apply()

operator_dict["/"] = DivNode