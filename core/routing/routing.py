import builtins

import re

from functools import reduce

from tokenizer import app, Tokenizer


def set_global_class(tag, number):
    str_exec = ""
    for i in range(number):
        str_exec += "builtins." + tag + "_" + str(i) + " = None\n"

    exec(str_exec)


def route(url, methods=["GET"], base_class="Tokenizer"):
    def wrapper(cls):
        urls = []

        urls.append("/" + cls.__name__.lower())

        def classtree(cls, prev_name=""):
            cls_name_arr = cls.__name__.split('_')

            if (len(cls_name_arr) > 1):
                name = reduce(lambda x, y: (x + '.' + y), cls_name_arr[1:])
            else:
                name = cls.__name__

            prev_name += "/" + name.lower()

            cls_childs = [value for key, value in cls.__dict__.items(
            ) if re.match(r"<class", str(value))]
            for child in cls_childs:
                urls.append(classtree(child, prev_name))

            return prev_name

        classtree(cls)

        set_global_class("NewClass", len(urls))

        str_exec = ""
        counter = 0
        for url in urls:
            last_slash_index = url.rfind("/") + 1
            new_url = url[:last_slash_index] + \
                "(" + url[last_slash_index:] + ")"

            str_exec += "global NewClass_" + \
                str(counter) + "\nclass NewClass_" + \
                str(counter) + "(" + base_class + "):\n"
            str_exec += "    @app.route('" + new_url + \
                "', methods=" + str(methods) + \
                ")\n"
            str_exec += "    def get(self, *args):\n        super().get(*args)\n\n"
            str_exec += "NewClass_" + \
                str(counter) + " = NewClass_" + str(counter) + "\n\n"

            counter += 1

        exec(str_exec)

        return

    return wrapper
