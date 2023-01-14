from typing import Any, TYPE_CHECKING, List
from client.engine.primitives.command import Command
from .events import (
    SetProfileEvent,
    NewProfileEvent,
    ProfileSetInGameEvent,
    GetProfilesEvent,
    UpdateProfilesInGameEvent,
)

if TYPE_CHECKING:
    from client.engine.general_state.profile.profile import Profile


class SetProfile(Command):
    def __init__(self, profile: Any, queue: Any, key):
        super().__init__(profile, queue, f"Setting profile {key}")
        self.events = [
            SetProfileEvent(key),
        ]


class NewProfile(Command):
    def __init__(self, profile: Any, queue: Any):
        super().__init__(profile, queue, "Setting new profile")
        self.events = [
            NewProfileEvent(),
        ]


class ProfileIsSet(Command):
    def __init__(self, profile: Any, queue: Any, key):
        super().__init__(profile, queue, f"Profile set to {key}")
        self.events = [
            ProfileSetInGameEvent(key),
        ]


class GetProfiles(Command):
    def __init__(self, profile: Any, queue: Any):
        super().__init__(profile, queue, "Get Profiles List")
        self.events = [GetProfilesEvent()]


class UpdateProfiles(Command):
    def __init__(self, profile: Any, queue: Any, profiles: List[Profile]):
        super().__init__(profile, queue, "Profile list retrieved")
        self.events = [UpdateProfilesInGameEvent(profiles)]
