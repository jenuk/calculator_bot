from _token import token
from basic_bot import BasicBot
from parse import parse

class CalculatorBot(BasicBot):
    def __init__(self, token):
        super().__init__(token)
        self.handler = {"message":self.reply}

    def reply(self, message):
        options = {"chat_id":message["chat"]["id"]}
        if message["text"].startswith("/"):
            if message["text"].startswith("/start"):
                text = ("Welcome to my awesome Bot.\n"
                    "You can find the code at <a>https://github.com/jenuk/calculator_bot</a>.\n"
                    "This bot can evaluate simple mathematical expression.")
                options["parse_mode"] = "HTML"
            if message["text"].startswith("/help"):
                text = ("You can use decimal numbers, parentheses and the operators *, /, +, -.\n"
                    "Request additional operations with /request and a description of the desired change.")
            if message["text"].startswith("/request"):
                text = "Your suggestion was saved for later review."
                with open("suggestions.txt", "a") as file:
                    file.write("{}: {}".format(message["from"]["id"], message["text"][9:]))
        else:
            orig = message["text"]
            symb = "$"
            text = ""
            poss = []
            err = False

            if symb not in orig:
                orig = symb + orig + symb

            for k in range(len(orig)):
                if orig[k] == symb:
                    poss.append(k)

            if len(poss) % 2 != 0:
                text = "Uneven number of {}s".format(symb)
                poss = []
                err = True

            last = 0
            for k in range(0, len(poss)-1, 2):
                try:
                    num, tree = self.calculate(orig[poss[k]+1:poss[k+1]])
                    text += orig[last:poss[k]] + "{} = {}".format(tree, num)
                    last = poss[k+1]+1
                except ArithmeticError as e:
                    text = "There was an error while evaulating your expression: {}".format(e)
                    err = True
                    break

            if not err:
                text += orig[last:]

        options["text"] = text
        self.send_message(**options)

    def calculate(self, expression):
        tree = parse(expression)
        return tree.apply(), tree

if __name__ == '__main__':
    bot = CalculatorBot(token)
    bot.loop(3)