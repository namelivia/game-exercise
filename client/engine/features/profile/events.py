from typing import TYPE_CHECKING, List
from client.engine.primitives.event import Event, InGameEvent

if TYPE_CHECKING:
    from client.engine.general_state.profile.profile import Profile


class SetProfileEvent(Event):
    def __init__(self, key: str):
        super().__init__()
        self.key = key


class NewProfileEvent(Event):
    pass


class ProfileSetInGameEvent(InGameEvent):
    def __init__(self, key: str):
        super().__init__()
        self.key = key


class GetProfilesEvent(Event):
    pass


class ProfilesUpdatedEvent(Event):
    def __init__(self, profiles: List[Profile]):
        super().__init__()
        self.profiles = profiles


class UpdateProfilesInGameEvent(InGameEvent):
    def __init__(self, profiles: List[Profile]):
        super().__init__()
        self.profiles = profiles
