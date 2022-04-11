from client.primitives.command import Command
from .events import (
    QuitGameEvent,
    UserTypedEvent
)

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


class QuitGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, 'Exit from the game')

    def execute(self):
        self.queue.put(
            QuitGameEvent()
        )


class UserTyped(Command):
    def __init__(self, profile, queue, key):
        super().__init__(profile, queue, f'User typed key {key}')
        self.key = key

    def execute(self):
        self.queue.put(
            UserTypedEvent(self.key)
        )
