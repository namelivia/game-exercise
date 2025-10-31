from engine.primitives.event import Event

"""
Events contain an operation and the data needed in order to perform
the operation. Will be put on a queue and when handler will execute
that operation.
"""


class ScreenTransitionEvent(Event):
    def __init__(self, dest_screen: str):
        super().__init__()
        self.dest_screen = dest_screen
