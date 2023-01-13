from client.engine.primitives.event import InGameEvent


class UserTypedEvent(InGameEvent):
    def __init__(self, key):
        super().__init__()
        self.key = key
