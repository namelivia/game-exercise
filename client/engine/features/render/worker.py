import threading

from client.engine.backend.backend import Backend
from client.engine.backend.foundational_wrapper import FoundationalClock
from client.engine.backend.graphics.graphics import GraphicsBackend
from client.engine.general_state.current_screen import CurrentScreen


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
        window = GraphicsBackend.get().get_new_window(640, 480)
        while not self.stop_event.is_set():
            screen = CurrentScreen().get_current_screen()
            if screen is not None:
                GraphicsBackend.get().clear_window(window)
                screen.render(window)
                GraphicsBackend.get().update_display()
            self.clock.tick(60)  # 60 FPS
        print(f"[{self.name}] Thread successfully terminated and exited run().")

    def stop(self):
        self.stop_event.set()
