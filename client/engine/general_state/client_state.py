import uuid
from typing import TYPE_CHECKING, Optional

from client.engine.persistence.persistence import Persistence

from .clock import Clock
from .profile.factory import Factory
from .queue import Queue

if TYPE_CHECKING:
    from client.engine.general_state.profile.profile import Profile
    from client.engine.primitives.event import Event
    from client.engine.primitives.screen import Screen


class ClientState:
    def __init__(self, initial_event: "Event", profile_key: str):
        self.queue = Queue()
        self.profile = self._initialize_status(profile_key)
        self.clock = Clock()
        self.current_screen: Optional["Screen"] = None
        self.queue = Queue()
        self.queue.put(initial_event)

    def _get_new_profile(self, profile_key: str) -> "Profile":
        profile = Factory.new_profile(profile_key)
        profile.save()
        return profile

    def _initialize_status(self, profile_key: str) -> "Profile":
        try:
            return Persistence.load(profile_key)
        except FileNotFoundError:
            return self._get_new_profile(profile_key)

    def get_current_screen(self) -> Optional["Screen"]:
        return self.current_screen

    def set_current_screen(self, current_screen: "Screen") -> None:
        self.current_screen = current_screen

    def set_profile(self, profile_key: str) -> None:
        self.profile = self._initialize_status(profile_key)

    def new_profile(self) -> "Profile":  # Generate a new profile with a random name
        return self._get_new_profile(str(uuid.uuid4()))
