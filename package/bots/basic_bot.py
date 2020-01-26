import requests
from itertools import count

class BasicBot:
    def __init__(self, token):
        self.base = "https://api.telegram.org/bot" + token + "/"
        me = self.get_me()
        if not me["ok"]:
            raise RuntimeError("Inital communitcation with telegram server failed")
        self.name = me["result"]["first_name"]
        self.id = me["result"]["id"]
        self.username = me["result"]["username"]
        print("Hello, here is {}".format(self.name))
        self.offset = 0
        self.handler = dict()

    def request(self, command, values=None, filename=None):
        url = self.base + command

        if values is None or len(values) == 0:
            response = requests.get(url)
        elif filename is not None:
            files = {"photo": open("./images/"+filename, "rb").read()}
            response = requests.post(url, files=files, data=values)
        else:
            response = requests.post(url, json=values)

        if response:
            response.encoding = "utf-8"
            result = response.json()
        else:
            print("\n\n")
            print(response.status_code, response.reason)
            print(self.base + command)
            print(values)
            print("\n\n")
            response.raise_for_status()

        return result

    def method(self, m, **kwargs):
        return self.request(m, kwargs)

    def get_me(self):
        return self.method("getMe")

    def get_updates(self, **kwargs):
        return self.method("getUpdates", **kwargs)

    def send_message(self, **kwargs):
        return self.method("sendMessage", **kwargs)

    def send_photo(self, filename, **kwargs):
        return self.request("sendPhoto", kwargs, filename=filename)

    def answer_inline_query(self, querry, results):
        if type(results) == dict:
            results = [results]
        options = {"inline_query_id": querry["id"],
                   "results": results,}

        return self.method("answerInlineQuery", **options)

    def register(self, typ, func):
        self.handler[typ] = func
        return func

    def loop(self, iterations = 10):
        if len(self.handler) == 0:
            raise NotImplementedError("No functions to handle replies defined. You should add handlers to 'self.handler' dictionary")

        if iterations is None:
            print("Will now listen for messages")
            it = count()
        else:
            print("Will now listen for {} messages".format(iterations))
            it = range(iterations)

        for k in it:
            updates = self.get_updates(timeout=60, allowed_updates=list(self.handler.keys()))
            if not updates["ok"]:
                raise RuntimeError
            updates = updates["result"]
            if len(updates) == 0:
                print("-", end="", flush=True)
            for update in updates:
                keys = list(update.keys())
                typ = keys[1 ^ keys.index("update_id")]
                if self.handler[typ](update[typ]):
                    print(".", end="", flush=True)
                else:
                    print("*", end="", flush=True)
                self.offset = update["update_id"] + 1
            self.get_updates(offset=self.offset)
        print()