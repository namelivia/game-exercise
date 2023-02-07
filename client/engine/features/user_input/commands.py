from typing import TYPE_CHECKING

from client.engine.primitives.command import Command

from .events import UserTypedEvent

if TYPE_CHECKING:
    from client.engine.general_state.profile.profile import Profile
    from client.engine.general_state.queue import Queue


class UserTyped(Command):
    def __init__(self, profile: "Profile", queue: "Queue", key: str):
        super().__init__(profile, queue, f"User typed key {key}")
        self.events = [UserTypedEvent(key)]
