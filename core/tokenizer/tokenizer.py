import logging
import re

from tornado.escape import json_decode, json_encode
from tornado.web import HTTPError

from libs.frouting.frouting import RequestRoutingHandler, RoutingApplication

logging.basicConfig(filename="server.log", level=logging.DEBUG)

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
        except Exception:
            self._items = {}
            self._items["__counter"] = -1

    def _match(self, rule, path):
        sub_paths = path[path.find(":")].split('/')[1:]
        sub_rules = rule[1:].split('/')

        n_rule = len(sub_rules)
        n_path = len(sub_paths)
        reg_exp1 = r"<\w+>"
        reg_exp2 = r"\w+"
        if (n_rule == n_path):
            for i in range(n_rule):
                if ((re.match(reg_exp1, sub_rules[i]) and
                     re.match(reg_exp2, sub_paths[i])) or
                        re.match(sub_rules[i], sub_paths[i])):
                    continue
                else:
                    return False

            return True
        else:
            return False

    def _get_func_name(self):
        print(1)
        full_class_name = self.__module__ + '.' + self.__class__.__name__
        rule, func_name = self.application.handler_map.get(
            full_class_name, {}).get(self.request.method, (None, None))

        if not rule or not func_name:
            raise HTTPError(404, "")

        match = re.match(rule, self.request.path) or self._match(
            rule, self.request.path)
        if match:
            return func_name
        else:
            raise HTTPError(404, "")

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

    def get(self, *args):
        paths = self.request.uri[1:].split('/')

        if (len(paths) != 5):
            self.write(
                "<html><title>{0}: {1}</title><body>{0}: {1}</body></html>".format("403", "Forbidden"))
        else:
            token = self._get_token(paths)
            self.write({'token': token})
