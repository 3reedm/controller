from tornado.escape import json_decode, json_encode
from tornado_routing import RoutingApplication, RequestRoutingHandler

app = RoutingApplication()


class Tokenizer(RequestRoutingHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_data()
        self._changed = False

    def __del__(self):
        if (self._changed):
            with open("data.json", 'w') as file:
                file.write(json_encode(self._items))

    def _load_data(self):
        self._items = None

        try:
            with open("data.json") as file:
                self._items = json_decode(file.read())
        except Exception as e:
            self._items = {}
            self._items["__counter"] = -1

    def _get_token(self, path):
        new_attr = False
        child_items = self._items

        for i in path:
            if (new_attr):
                child_items[i] = {}
            elif (child_items.get(i) is None):
                child_items[i] = {}
                new_attr = True
                self._changed = True

            if (i != path[-1]):
                child_items = child_items[i]

        if (new_attr):
            self._items["__counter"] += 1
            child_items[path[-1]] = str(self._items["__counter"]).zfill(4)

        return child_items[path[-1]]

    @app.route(r'/api/([^/]+)/([^/]+)/([^/]+)/([^/]+)/?', methods=['GET'])
    def get_token(self, *path):
        token = self._get_token(path)
        self.write({'token': token})
