from typing import Dict, List
from client.engine.primitives.event import Event, InGameEvent


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
    def __init__(self, profiles: Dict[str, str]):
        super().__init__()
        self.profiles = profiles


class UpdateProfilesInGameEvent(InGameEvent):
    def __init__(self, profiles: List[Dict[str, str]]):
        super().__init__()
        self.profiles = profiles
