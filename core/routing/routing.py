import re

from functools import reduce

from tokenizer import app


def route(url, methods=["GET"], module_name="tokenizer", class_name="Tokenizer"):
    def wrapper(cls):
        urls = []

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

        str_exec = "class " + class_name + ":\n"
        for url in urls:
            last_slash_index = url.rfind("/") + 1
            url = url[:last_slash_index] + "(" + url[last_slash_index:] + ")"
            str_exec += "    @app.route('" + url + \
                "', methods=" + str(methods) + \
                ", module='" + module_name + "', cls='" + \
                class_name + "')\n"
        str_exec += "    def get(self, *args):\n        pass\n\n"

        return exec(str_exec)

    return wrapper


@route("/")
class API:
    class V1:
        class Portal:
            class Version_1_4:
                class Redaction_2:
                    pass

    class V2:
        pass
