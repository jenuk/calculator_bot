from ..node import Node

class NumberNode(Node):
    symb = ""
    priority = 100
    arguments = 0
    acts_as_number = True

    def __init__(self, value):
        super().__init__()
        self.value = value

    def apply(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.value)