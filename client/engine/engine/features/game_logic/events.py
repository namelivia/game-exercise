from engine.primitives.event import Event


class ChangeCursorEvent(Event):
    def __init__(self, key: str):
        super().__init__()
        self.key = key
