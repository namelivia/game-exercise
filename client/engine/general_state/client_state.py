from .clock import Clock
from .queue import Queue
from .profile.profile import Profile
from client.engine.persistence.persistence import Persistence
from .profile.factory import Factory


class ClientState:
    def __init__(self, initial_event, profile_key):
        self.queue = Queue()
        self.profile = self._initialize_status(profile_key)
        self.clock = Clock()
        self.current_screen = None
        self.queue = Queue()
        self.queue.put(initial_event)

    def _get_new_profile(self, profile_key) -> Profile:
        profile = Factory.new_profile(profile_key)
        profile.save()
        return profile

    def _initialize_status(self, profile_key) -> Profile:
        try:
            return Persistence.load(profile_key)
        except FileNotFoundError:
            return self._get_new_profile(profile_key)

    def get_current_screen(self):
        return self.current_screen

    def set_current_screen(self, current_screen):
        self.current_screen = current_screen
