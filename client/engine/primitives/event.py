import uuid
from abc import ABC


class Event(ABC):
    pass


class InGameEvent(Event):
    def __init__(self):
        self.id = uuid.uuid4()
