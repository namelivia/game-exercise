import threading
from queue import Empty

import pygame

from client.engine.external.foundational_wrapper import FoundationalClock
from client.engine.general_state.current_screen import CurrentScreen
from client.engine.graphics.graphics import Graphics


class StopThread(Exception):
    """Exception raised to signal a thread to stop processing."""

    pass


class RenderWorker(threading.Thread):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.current_screen = CurrentScreen()
        self.clock = FoundationalClock()
        # Event used to signal the thread to stop gracefully
        self.stop_event = threading.Event()
        # Log that the worked has started?

    def run(self):
        """The main execution loop for the thread."""
        print(f"[{self.name}] Thread started, waiting for events...")
        pygame.init()
        self.graphics = Graphics()
        while not self.stop_event.is_set():
            try:
                screen = self.current_screen.get_current_screen()
                if screen is not None:
                    self.graphics.render(screen)
            except Empty:
                continue
            except StopThread:
                # Internal exception to cleanly exit the loop
                break
            except Exception as e:
                print(f"Error {e}")
                break
            self.clock.tick(60)  # 60 FPS
