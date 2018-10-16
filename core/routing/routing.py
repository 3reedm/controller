from functools import reduce

from tokenizer import Tokenizer
from tornado_routing import RoutingApplication

app = RoutingApplication()


def route(rule, methods=['GET'], handler=Tokenizer):
    def wrap(cls):
        cls_name_arr = cls.__name__.split('_')

        if (len(cls_name_arr) > 1):
            name = reduce(lambda x, y: (x + '.' + y), cls_name_arr[1:])
        else:
            name = cls.__name__

        new_rule = rule + '/' + name + '/(.*)'

        class MagicTokenizer(cls):
            @app.route(new_rule, methods)
            def get(self, *args):
                super().get(*args)

        return MagicTokenizer

    return wrap


@route('/', methods=['GET'])
class API:
    @route('/api', methods=['GET'])
    class V1:
        @route('/api/v1', methods=['GET'])
        class Portal:
            @route('/api/v1/portal', methods=['GET'])
            class Version_1_4:
                @route('/api/v1/portal/1.4', methods=['GET'])
                class Redaction_2:
                    pass

    @route('/api', methods=['GET'])
    class V2:
        pass
