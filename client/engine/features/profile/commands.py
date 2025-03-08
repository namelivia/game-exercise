from typing import TYPE_CHECKING, Dict, List

from client.engine.primitives.command import Command

from .events import (
    GetProfilesEvent,
    NewProfileEvent,
    ProfileSetInGameEvent,
    SetProfileEvent,
    UpdateProfilesInGameEvent,
)

if TYPE_CHECKING:
    from client.engine.general_state.profile.profile import Profile
    from client.engine.general_state.queue import Queue


class SetProfile(Command):
    def __init__(self, queue: "Queue", key: str):
        super().__init__(queue, f"Setting profile {key}")
        self.events = [
            SetProfileEvent(key),
        ]


class NewProfile(Command):
    def __init__(self, queue: "Queue"):
        super().__init__(queue, "Setting new profile")
        self.events = [
            NewProfileEvent(),
        ]


class ProfileIsSet(Command):
    def __init__(self, queue: "Queue", key: str):
        super().__init__(queue, f"Profile set to {key}")
        self.events = [
            ProfileSetInGameEvent(key),
        ]


class GetProfiles(Command):
    def __init__(self, queue: "Queue"):
        super().__init__(queue, "Get Profiles List")
        self.events = [GetProfilesEvent()]


class UpdateProfiles(Command):
    def __init__(self, queue: "Queue", profiles: List[Dict[str, str]]):
        super().__init__(queue, "Profile list retrieved")
        self.events = [UpdateProfilesInGameEvent(profiles)]
