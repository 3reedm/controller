class Controller:
    def __init__(self, server=None, client=None):
        self.server = server if server else TornadoServer()
        self.client = client if client else Client()
        self.options = self.server.get_options()

        self.start()

    def __del__(self):
        self.stop()

    def __enter__(self):
        self.server.start()
        self.client.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.stop()
        self.client.stop()

        if exc_val:
            raise

    def start(self):
        self.server.start()
        self.client.start()

    def stop(self):
        self.server.stop()
        self.client.stop()
