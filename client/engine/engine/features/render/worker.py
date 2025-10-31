import threading
from queue import Empty

from engine.backend.backend import Backend
from engine.backend.graphics.graphics import GraphicsBackend
from engine.clock import Clock
from engine.primitives.event import StopThreadEvent

from .event_handler import handlers_map
from .state import State


class RenderWorker(threading.Thread):

    def __init__(self, name, queue):
        super().__init__()
        self.name = name
        self.stop_event = threading.Event()
        self.queue = queue

    def _render_next_frame(self, screen, window):
        if screen is not None:
            GraphicsBackend.get().clear_window(window)
            screen.render(window)
            GraphicsBackend.get().update_display()
        Clock().tick(60)  # 60 FPS

    def run(self):
        """The main execution loop for the thread."""
        print(f"[{self.name}] Thread started, waiting for events...")
        Backend.init()
        window = GraphicsBackend.get().get_new_window(640, 480)
        state = State()
        state.initialize()
        while not self.stop_event.is_set():
            self._render_next_frame(state.get_current_screen(), window)
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
