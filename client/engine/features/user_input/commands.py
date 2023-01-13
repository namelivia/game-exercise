from client.engine.primitives.command import Command
from .events import (
    UserTypedEvent,
)


class UserTyped(Command):
    def __init__(self, profile, queue, key):
        super().__init__(profile, queue, f"User typed key {key}")
        self.key = key

    def execute(self):
        self.queue.put(UserTypedEvent(self.key))
