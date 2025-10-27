from client.engine.primitives.command import Command

from .events import UserClickedEvent, UserTypedEvent


class UserTyped(Command):
    def __init__(self, key: str) -> None:
        super().__init__(f"User typed key {key}")
        self.events = [UserTypedEvent(key)]


class UserClicked(Command):
    def __init__(self) -> None:
        super().__init__(f"User clicked")
        self.events = [UserClickedEvent()]
