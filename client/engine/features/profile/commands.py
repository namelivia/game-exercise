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


class SetProfile(Command):
    def __init__(self, key: str) -> None:
        super().__init__(f"Setting profile {key}")
        self.events = [
            SetProfileEvent(key),
        ]


class NewProfile(Command):
    def __init__(self) -> None:
        super().__init__("Setting new profile")
        self.events = [
            NewProfileEvent(),
        ]


class ProfileIsSet(Command):
    def __init__(self, key: str) -> None:
        super().__init__(f"Profile set to {key}")
        self.events = [
            ProfileSetInGameEvent(key),
        ]


class GetProfiles(Command):
    def __init__(self) -> None:
        super().__init__("Get Profiles List")
        self.events = [GetProfilesEvent()]


class UpdateProfiles(Command):
    def __init__(self, profiles: List[Dict[str, str]]) -> None:
        super().__init__("Profile list retrieved")
        self.events = [UpdateProfilesInGameEvent(profiles)]
