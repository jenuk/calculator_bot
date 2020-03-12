from ..node import Node, operator_dict
from .number import NumberNode

class AddNode(Node):
    symb = "+"
    arguments = 2
    priority = 0
    acts_as_number = False

    def apply(self):
        if self.first is None:
            raise MalformedExpressionException("Not enough arguments for addition")
        res = self.first.apply()
        for child in self.children[1:]:
            res = res + child.apply()
        return res

    def simplify(self):
        new_children = []
        for child in self.children:
            child = child.simplify()
            if type(child) == AddNode:
                new_children.extend(child.children)
            else:
                new_children.append(child)

        self.children = new_children
        new_children = []

        nn = None # numbernode
        for child in self.children:
            if type(child) == NumberNode:
                if nn is None:
                    nn = child
                    new_children.append(child)
                else:
                    nn.value = nn.value + child.value
            else:
                new_children.append(child)

        self.children = new_children

        if len(self.children) == 1:
            return self.first
        else:
            return self

operator_dict["+"] = AddNode