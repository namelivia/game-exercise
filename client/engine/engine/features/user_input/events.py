from engine.primitives.event import Event, InGameEvent


class UserTypedEvent(InGameEvent):
    def __init__(self, key: str):
        super().__init__()
        self.key = key


class UserClickedEvent(InGameEvent):
    pass


class DisableUserInputEvent(Event):
    pass
