from typing import List

from client.engine.primitives.event import InGameEvent


class UserTypedEvent(InGameEvent):
    def __init__(self, key: str):
        super().__init__()
        self.key = key


class UserClickedEvent(InGameEvent):
    def __init__(self, coordinates: List[int]):
        super().__init__()
        self.coordinates = coordinates
