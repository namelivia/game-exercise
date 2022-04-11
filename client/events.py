from client.primitives.event import Event

"""
Events contain an operation and the data needed in order to perform
the operation. Will be put on a queue and when handler will execute
that operation.
"""


class QuitGameEvent(Event):
    pass

class UserTypedEvent(Event):
    def __init__(self, key):
        super().__init__()
        self.key = key
