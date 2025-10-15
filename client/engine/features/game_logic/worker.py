import threading
from queue import Empty

from client.engine.features.game_logic.event_handler import handlers_map
from client.engine.general_state.current_screen import CurrentScreen
from client.engine.primitives.event import InGameEvent, StopThreadEvent


class StopThread(Exception):
    """Exception raised to signal a thread to stop processing."""

    pass


class GameLogicWorker(threading.Thread):

    def __init__(self, name, queue):
        super().__init__()
        self.name = name
        self.queue = queue
        # Log that the worked has started?

    def run(self):
        """The main execution loop for the thread."""
        print(f"[{self.name}] Thread started, waiting for events...")
        while True:
            try:
                event = self.queue.get()
                if type(event) is StopThreadEvent:
                    break
                else:
                    # TODO: Events processor is missing here
                    # I was using it to combine the base
                    # event handler with the custom event
                    # handler from the game.
                    # The screen transition event belongs
                    # to the game so the kickstart code is
                    # crashing now
                    if event is not isinstance(event, InGameEvent):
                        handlers_map[type(event)]().handle(event)
                    else:
                        current_screen = CurrentScreen().get_current_screen()
                        if current_screen is not None:
                            current_screen.update_events(event)
            except Empty:
                continue
        print(f"[{self.name}] Thread successfully terminated and exited run().")

    def stop(self):
        self.queue.put(StopThreadEvent())
