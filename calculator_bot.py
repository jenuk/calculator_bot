from _token import token
from basic_bot import BasicBot

class CalculatorBot(BasicBot):
    def __init__(self, token):
        super().__init__(token)
        self.handler = {"message":self.reply}


    def reply(self, message):
        if message["text"].startswith("/start"):
            text = "Welcome to my awesome Bot.\nSadly it can't do anything at the moment"
        else:
            text = "Hello, this is message number {}".format(message["message_id"])
        self.send_message(chat_id=message["chat"]["id"], text=text)

if __name__ == '__main__':
    bot = CalculatorBot(token)