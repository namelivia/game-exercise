import uuid
from abc import ABC


class Event(ABC):
    pass


# This is an special type of event used to stop a thread
# when exiting the program.
class StopThreadEvent(Event):
    pass


class InGameEvent(Event):
    def __init__(self) -> None:
        self.id = uuid.uuid4()
