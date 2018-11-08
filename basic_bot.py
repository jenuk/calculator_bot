from _token import token
import urllib.parse
import urllib.request
import urllib.error
import json
from itertools import count

class BasicBot:
    def __init__(self, token):
        self.base = "https://api.telegram.org/bot" + token + "/"
        me = self.get_me()
        if not me["ok"]:
            raise NotImplementedError
        self.name = me["result"]["first_name"]
        self.id = me["result"]["id"]
        self.username = me["result"]["username"]
        self.offset = 0
        self.handler = dict()

    def request(self, command, values=None):
        url = self.base + command
        if values is None or len(values) == 0:
            req = url
        else:
            data = urllib.parse.urlencode(values).encode("utf-8")
            req = urllib.request.Request(url, data)

        try:
            with urllib.request.urlopen(req) as respone:
                result = json.loads(respone.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(self.base + command)
            raise e

        return result

    def method(self, m, **kwargs):
        return self.request(m, kwargs)

    def get_me(self):
        return self.method("getMe")

    def get_updates(self, **kwargs):
        return self.method("getUpdates", **kwargs)

    def send_message(self, **kwargs):
        return self.method("sendMessage", **kwargs)

    def register(self, typ, func):
        self.handler[typ] = func
        return func

    def loop(self, iterations = 2):
        if len(self.handler) == 0:
            raise NotImplementedError("No functions to handle replies defined")

        if iterations is None:
            it = count()
        else:
            it = range(iterations)

        for k in it:
            updates = self.get_updates(timeout=60, allowed_updates=self.handler.keys())
            if not updates["ok"]:
                raise RuntimeError
            updates = updates["result"]
            for update in updates:
                keys = list(update.keys())
                typ = keys[1 ^ keys.index("update_id")]
                self.handler[typ](update[typ])
                self.offset = update["update_id"] + 1
            self.get_updates(offset=self.offset)


if __name__ == '__main__':
    bot = BasicBot(token)