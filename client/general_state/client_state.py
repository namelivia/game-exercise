from .clock import Clock
from .queue import Queue
from .profile.profile import Profile
from client.persistence.persistence import Persistence
from .profile.factory import Factory


class ClientState:
    def __init__(self, initial_event):
        self.queue = Queue()
        self.profile = self._initialize_status()
        self.clock = Clock()
        self.current_screen = None
        self.queue = Queue()
        self.queue.put(initial_event)

    def _get_new_profile(self) -> Profile:
        name = input("Enter your name:")
        profile = Factory.new_profile(name)
        profile.save()
        return profile

    def _initialize_status(self) -> Profile:
        try:
            return Persistence.load()
        except FileNotFoundError:
            return self._get_new_profile()

    def get_current_screen(self):
        return self.current_screen

    def set_current_screen(self, current_screen):
        self.current_screen = current_screen
