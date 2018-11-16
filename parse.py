from tree import *
from number import Number
from error import MalformedExpressionException

def parse(expression):
    ops = list(operator_dict.keys())
    root_stack = [ParenthesesNode(True)]
    root = root_stack[-1]

    expression = expression.replace(" ", "")
    token_list = []
    last_token = "open"
    for ch in expression:
        if ch == "(":
            last_token = "open"
            token_list.append([last_token, ch])
        elif ch == ")":
            last_token = "close"
            token_list.append([last_token, ch])
        elif last_token == "open" and ch == "-":
            last_token = "number"
            token_list.append([last_token, ch])
        elif ch in "01234567890.":
            if last_token == "number":
                token_list[-1][1] += ch
            else:
                last_token = "number"
                token_list.append([last_token, ch])
        elif ch in ops:
            last_token = "operator"
            token_list.append([last_token, ch])
        else:
            raise MalformedExpressionException("Undefined symbol: {}".format(ch))

    for kind, token in token_list:
        if kind == "open":
            node = ParenthesesNode()
            root.insert(node)
            root_stack.append(node)
            root = node
            continue
        elif kind == "close":
            if not root.verify():
                raise MalformedExpressionException("Incomplete expression in a parentheses")
            root_stack.pop()
            if len(root_stack) == 0:
                raise MalformedExpressionException("Too many closing parentheses")
            root = root_stack[-1]
            continue

        if kind == "number":
            node = NumberNode(Number(string=token))
        elif kind == "operator":
            node = operator_dict[token]()

        root.insert(node)

    if len(root_stack) > 1:
        raise MalformedExpressionException("Too many opening parentheses")
    if not root.verify():
        raise MalformedExpressionException("Incomplete expression")

    return root_stack[0]