from engine.threading.polling_worker import PollingWorker

from .backend.pygame.input import InputBackend
from .commands import UserClicked, UserTyped
from .keyboard import KeyboardInput
from .mouse import MouseInput


class UserInputWorker(PollingWorker):

    IDLE_TIME = 0.005

    def __init__(self, name):
        super().__init__(name)
        self.keyboard_input = KeyboardInput()
        self.mouse_input = MouseInput()

    def step(self):
        events = InputBackend.get_event()
        keyboard_events = self.keyboard_input.read(events)
        for keyboard_event in keyboard_events:
            UserTyped(keyboard_event).execute()
        mouse_event = self.mouse_input.read(events)
        if mouse_event is not None:
            UserClicked().execute()
