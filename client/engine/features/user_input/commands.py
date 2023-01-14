from typing import Any
from client.engine.primitives.command import Command
from .events import (
    UserTypedEvent,
)


class UserTyped(Command):
    def __init__(self, profile: Any, queue: Any, key: str):
        super().__init__(profile, queue, f"User typed key {key}")
        self.events = [UserTypedEvent(key)]
