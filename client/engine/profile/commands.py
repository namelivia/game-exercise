from client.engine.primitives.command import Command
from .events import (
    SetProfileEvent,
    NewProfileEvent,
    ProfileSetInGameEvent,
)


class SetProfile(Command):
    def __init__(self, profile, queue, key):
        super().__init__(profile, queue, f"Setting profile {key}")
        self.events = [
            SetProfileEvent(key),
        ]


class NewProfile(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Setting new profile")
        self.events = [
            NewProfileEvent(),
        ]


class ProfileIsSet(Command):
    def __init__(self, profile, queue, key):
        super().__init__(profile, queue, f"Profile set to {key}")
        self.events = [
            ProfileSetInGameEvent(key),
        ]
