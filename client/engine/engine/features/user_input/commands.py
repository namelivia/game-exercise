from engine.primitives.command import Command

from .events import (
    DisableUserInputEvent,
    EnableUserInputEvent,
    UserClickedEvent,
    UserTypedEvent,
)


class UserTyped(Command):
    def __init__(self, key: str) -> None:
        super().__init__(f"User typed key {key}")
        self.events = [UserTypedEvent(key)]


class UserClicked(Command):
    def __init__(self) -> None:
        super().__init__(f"User clicked")
        self.events = [UserClickedEvent()]


class DisableUserInput(Command):
    def __init__(self) -> None:
        super().__init__(f"Disable user input")
        self.queue = "user_input"
        self.events = [
            DisableUserInputEvent(),
        ]


class EnableUserInput(Command):
    def __init__(self) -> None:
        super().__init__(f"Disable user input")
        self.queue = "user_input"
        self.events = [
            EnableUserInputEvent(),
        ]
