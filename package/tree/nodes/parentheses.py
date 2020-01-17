from ..node import Node

class ParenthesesNode(Node):
    symb = "()"
    priority = 100
    arguments = 1
    acts_as_number = True

    def __init__(self, is_root=False):
        super().__init__()
        self.is_root = is_root

    def apply(self):
        return self.first.apply()

    def __str__(self):
        if self.is_root:
            return str(self.first)
        else:
            return "({})".format(self.first)