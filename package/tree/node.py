from ..extra.error import MalformedExpressionException

operator_dict = {}

class Node:
    symb = None
    arguments = 0
    priority = 0
    acts_as_number = False
    show_implied_parentheses = False

    def __init__(self):
        self.children = []
        self.pos = (0, 0) # used for drawing the graph

    def apply(self):
        raise NotImplementedError()

    def simplify(self):
        for child in self.children:
            child.simplify()

    def insert(self, node):
        if len(self.children) < self.arguments:
            self.children.append(node)
        elif self.last.priority >= node.priority:
            if node.acts_as_number:
                print(self, node)
                raise MalformedExpressionException("Too many arguments for {} operator".format(self.symb))
            if not self.last.verify():
                raise MalformedExpressionException("Not enough arguments for {} operator".format(self.last.symb))
            node.first = self.last
            self.last = node
        else:
            self.last.insert(node)

    def verify(self):
        if len(self.children) != self.arguments:
            return False

        for child in self.children:
            if not child.verify():
                return False

        return True

    def __str__(self):
        if self.arguments == 2:
            if self.show_implied_parentheses:
                return "({} {} {})".format(self.first, self.symb, self.last)
            else:
                return "{} {} {}".format(self.first, self.symb, self.last)
        else:
            res = "{}(".format(self.symb)
            res += ", ".join(map(str, self.children))
            res += ")"
            return res

    def __repr__(self):
        return "{}(".format(type(self).__name__) + ", ".join(map(repr, self.children)) + ")"

    @property
    def first(self):
        if self.arguments == 0:
            raise TypeError("{} has no children".format(type(self).__name__))
        if len(self.children) == 0:
            return None
        else:
            return self.children[0]

    @first.setter
    def first(self, arg):
        if self.arguments == 0:
            raise TypeError("{} should not have any children".format(type(self).__name__))

        if len(self.children) == 0:
            self.children.append(arg)
        else:
            self.children[0] = arg

    @property
    def last(self):
        if self.arguments == 0:
            raise TypeError("{} has no (last) child".format(type(self).__name__))
        if len(self.children) < self.arguments:
            return None
        else:
            return self.children[-1]

    @last.setter
    def last(self, arg):
        if self.arguments == 0:
            raise TypeError("{} should not have a (last) child".format(type(self).__name__))

        if len(self.children) < self.arguments:
            self.children.append(arg)
        else:
            self.children[-1] = arg