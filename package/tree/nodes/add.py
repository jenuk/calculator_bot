from ..node import Node, operator_dict

class AddNode(Node):
    symb = "+"
    arguments = 2
    priority = 0
    acts_as_number = False

    def apply(self):
        if self.first is None or self.last is None:
            raise MalformedExpressionException("Not enough arguments for addition")
        return self.first.apply() + self.last.apply()

operator_dict["+"] = AddNode