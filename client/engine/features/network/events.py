from client.engine.primitives.event import Event


class NetworkRequestEvent(Event):
    def __init__(self, data):
        super().__init__()
        self.data = data
