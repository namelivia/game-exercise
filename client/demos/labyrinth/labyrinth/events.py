from engine.api import InGameEvent


class SetCustomCursorEvent(InGameEvent):
    def __init__(self, key: str):
        super().__init__()
        self.key = key
