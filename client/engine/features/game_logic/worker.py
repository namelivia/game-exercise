import threading
from queue import Empty

from client.engine.features.game_logic.event_handler import EventHandler
from client.engine.features.game_logic.events_processor import EventsProcessor
from client.engine.features.game_logic.game_event_handler import GameEventHandler
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
        game_handler = GameEventHandler().get()
        events_processor = EventsProcessor(
            [game_handler, EventHandler()]  # Regular events and in game events
        )
        while True:
            try:
                event = self.queue.get()
                if type(event) is StopThreadEvent:
                    break
                else:
                    if not isinstance(event, InGameEvent):
                        if event is not None and not isinstance(event, InGameEvent):
                            events_processor.handle(event)
                    else:
                        current_screen = CurrentScreen().get_current_screen()
                        if current_screen is not None:
                            current_screen.update_events(event)
            except Empty:
                continue
        print(f"[{self.name}] Thread successfully terminated and exited run().")

    def stop(self):
        self.queue.put(StopThreadEvent())
