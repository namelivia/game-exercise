import threading
import time
from queue import Empty

from engine.primitives.event import StopThreadEvent

from .backend.pygame.input import InputBackend
from .commands import UserClicked, UserTyped
from .event_handler import handlers_map
from .keyboard import KeyboardInput
from .mouse import MouseInput
from .state import State


class UserInputWorker(threading.Thread):

    IDLE_TIME = 0.005

    def __init__(self, name, queue):
        super().__init__()
        self.name = name
        self.stop_event = threading.Event()
        self.queue = queue

        self.keyboard_input = KeyboardInput()
        self.mouse_input = MouseInput()

    def _read_user_input(self):
        events = InputBackend.get_event()
        keyboard_events = self.keyboard_input.read(events)
        for keyboard_event in keyboard_events:
            UserTyped(keyboard_event).execute()
        mouse_event = self.mouse_input.read(events)
        if mouse_event is not None:
            UserClicked().execute()
        time.sleep(UserInputWorker.IDLE_TIME)

    def run(self):
        print(f"[{self.name}] Thread started, waiting for events...")
        state = State()
        state.initialize()
        while not self.stop_event.is_set():
            if state.user_input_is_enabled():
                self._read_user_input()
            try:
                event = self.queue.get(timeout=0.001)
                if type(event) is StopThreadEvent:
                    break
                else:
                    handlers_map[type(event)]().handle(event)
            except Empty:
                continue
        print(f"[{self.name}] Thread successfully terminated and exited run().")

    def stop(self):
        self.stop_event.set()
