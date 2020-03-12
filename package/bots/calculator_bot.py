from .basic_bot import BasicBot
from .parse import parse
from ..visualize.visualize import draw

class CalculatorBot(BasicBot):
    def __init__(self, token):
        super().__init__(token)
        self.handler = {"message":self.reply, "inline_query":self.inline_query}

    def reply(self, message):
        options = {"chat_id":message["chat"]["id"]}
        sucess = True
        if message["text"].startswith("/"):
            if message["text"].startswith("/start"):
                text = ("Welcome to my awesome Bot.\n"
                    "You can find the code at <a>https://github.com/jenuk/calculator_bot</a>.\n"
                    "This bot can evaluate simple mathematical expression.")
                options["parse_mode"] = "HTML"
            elif message["text"].startswith("/help"):
                text = ("You can use decimal numbers, parentheses and the operators *, /, +, -, ^, %. "
                    "You can also perform multiple calculations in one message by placing the expressions in $...$.\n"
                    "For example: "
                    "'The area of a rectangle with side lengths 3 and 4 is $3*4$, the circumference is $2*(3+4)$'\n\n"
                    "Request additional operations with /request and a description of the desired change.")
            elif message["text"].startswith("/request"):
                text = "Your suggestion was saved for later review."
                with open("suggestions.txt", "a") as file:
                    file.write("{}: {}\n".format(message["from"]["id"], message["text"][9:]))
            elif message["text"].startswith("/debug"):
                try:
                    num, tree = self.calculate(message["text"][7:])
                except (ArithmeticError, TypeError) as e:
                    options["text"] = "There was an error while evaulating your expression: {}".format(e)
                    self.send_message(**options)
                    return False

                tree.simplify()
                draw(tree)
                options["caption"] = f"{message['text'][7:]} = {num}"
                self.send_photo("graph.png", **options)
                return True
            else:
                text = "I did not understand your querry"
                sucess = False
        else:
            text, sucess = self.translate_message(message["text"])


        options["text"] = text
        self.send_message(**options)

        return sucess

    def inline_query(self, query):
        result = {"type": "article",
                  "id": "std",
                  }

        text, sucess = self.translate_message(query["query"])
        result["title"] = text
        result["input_message_content"] =  {"message_text": text}


        self.answer_inline_query(query, result)

        return sucess

    def translate_message(self, orig):
        symb = "$"
        text = ""
        poss = []

        if symb not in orig:
            orig = symb + orig + symb

        for k in range(len(orig)):
            if orig[k] == symb:
                poss.append(k)

        if len(poss) % 2 != 0:
            text = "Uneven number of {}s".format(symb)
            return text, False

        last = 0
        for k in range(0, len(poss)-1, 2):
            try:
                num, tree = self.calculate(orig[poss[k]+1:poss[k+1]])
                text += orig[last:poss[k]] + "{} = {}".format(tree, num)
                last = poss[k+1]+1
            except (ArithmeticError, TypeError) as e:
                text = "There was an error while evaulating your expression: {}".format(e)
                return text, False

        text += orig[last:]

        return text, True


    def calculate(self, expression):
        if expression.lower().startswith("the answer"):
            return 42, expression
        tree = parse(expression)
        return tree.apply(), tree