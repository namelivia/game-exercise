import threading

from client.engine.backend.backend import Backend
from client.engine.backend.foundational_wrapper import FoundationalClock
from client.engine.general_state.current_screen import CurrentScreen
from client.engine.graphics.graphics import Graphics


class StopThread(Exception):
    """Exception raised to signal a thread to stop processing."""

    pass


class RenderWorker(threading.Thread):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.clock = FoundationalClock()
        # Event used to signal the thread to stop gracefully
        self.stop_event = threading.Event()
        # Log that the worked has started?

    def run(self):
        """The main execution loop for the thread."""
        print(f"[{self.name}] Thread started, waiting for events...")
        Backend.init()
        self.graphics = Graphics()
        while not self.stop_event.is_set():
            screen = CurrentScreen().get_current_screen()
            if screen is not None:
                self.graphics.render(screen)
            self.clock.tick(60)  # 60 FPS
        print(f"[{self.name}] Thread successfully terminated and exited run().")

    def stop(self):
        self.stop_event.set()
