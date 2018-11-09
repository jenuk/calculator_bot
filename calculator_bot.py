from _token import token
from basic_bot import BasicBot
from number import Number

class CalculatorBot(BasicBot):
    def __init__(self, token):
        super().__init__(token)
        self.handler = {"message":self.reply}
        self.symb = set(["*", "/", "+", "-"])
        self.numb = [str(i) for i in range(10)]
        self.numb.append(".")
        self.numb = set(self.numb)

    def reply(self, message):
        options = {"chat_id":message["chat"]["id"]}
        if message["text"].startswith("/"):
            if message["text"].startswith("/start"):
                text = ("Welcome to my awesome Bot.\n"
                    "You can find the code at <a>https://github.com/jenuk/calculator_bot</a>.\n"
                    "This bot can evaluate simple mathematical expression.")
                options["parse_mode"] = "HTML"
            if message["text"].startswith("/help"):
                text = ("You can use decimal numbers and the symbols *, /, +, -.\n"
                    "Request additional operations with /request and a description of the desired change.")
            if message["text"].startswith("/request"):
                text = "Your suggestion was saved for later review."
                with open("suggestions.txt", "a") as file:
                    file.write("{}: {}".format(message["from"]["id"], message["text"][9:]))
        else:
            try:
                res = self.calculate(message["text"])
                text = str(res)
            except ValueError:
                text = "Your message did not contain only math"
        options["text"] = text
        self.send_message(**options)

    def calculate(self, expression):
        expression = expression.replace(" ", "")
        if not set(expression).intersection(self.symb.union(self.numb)):
            raise ValueError("None mathematical symbol in expression")

        res = Number(0, 1)
        next_op = "+"
        if expression[0] == "-":
            next_op = "-"
            expression = expression[1:]
        i = 0
        for k, ch in enumerate(expression):
            if ch in self.symb:
                if i == k:
                    raise ValueError("Expression malformed")
                curr = Number(string=expression[i:k])
                res = self.apply(next_op, res, curr)
                next_op = expression[k]
                i = k+1
        curr = Number(string=expression[i:])
        res = self.apply(next_op, res, curr)

        return res

    def apply(self, op, n1, n2):
        if op == "*":
            return n1 * n2
        elif op == "/":
            return n1 / n2
        elif op == "+":
            return n1 + n2
        elif op == "-":
            return n1 - n2
        else:
            raise NotImplementedError("The {} operation is not implemented".format(op))

if __name__ == '__main__':
    bot = CalculatorBot(token)