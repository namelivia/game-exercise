import threading
from queue import Empty

from client.engine.backend.backend import Backend
from client.engine.backend.foundational_wrapper import FoundationalClock
from client.engine.backend.graphics.graphics import GraphicsBackend
from client.engine.features.render.event_handler import handlers_map
from client.engine.primitives.event import StopThreadEvent

from .state import State


class StopThread(Exception):
    """Exception raised to signal a thread to stop processing."""

    pass


class RenderWorker(threading.Thread):

    def __init__(self, name, queue):
        super().__init__()
        self.name = name
        self.clock = FoundationalClock()
        # Event used to signal the thread to stop gracefully
        self.stop_event = threading.Event()
        self.queue = queue
        # Log that the worked has started?

    def _render_next_frame(self, screen, window):
        if screen is not None:
            GraphicsBackend.get().clear_window(window)
            screen.render(window)
            GraphicsBackend.get().update_display()
        self.clock.tick(60)  # 60 FPS

    def run(self):
        """The main execution loop for the thread."""
        print(f"[{self.name}] Thread started, waiting for events...")
        Backend.init()
        window = GraphicsBackend.get().get_new_window(640, 480)
        state = State()
        state.initialize()
        while not self.stop_event.is_set():
            if state.get_is_rendering():  # Rendering mode
                self._render_next_frame(state.get_current_screen(), window)
            else:  # Queue mode
                try:
                    event = self.queue.get_for_workers()
                    if type(event) is StopThreadEvent:
                        break
                    else:
                        handlers_map[type(event)]().handle(event)
                except Empty:
                    continue
        print(f"[{self.name}] Thread successfully terminated and exited run().")

    def stop(self):
        self.stop_event.set()
