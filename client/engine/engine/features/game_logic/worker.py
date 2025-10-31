from engine.general_state.current_screen import CurrentScreen
from engine.primitives.event import InGameEvent
from engine.threading.queue_worker import QueueWorker

from .event_handler import EventHandler
from .events_processor import EventsProcessor
from .game_event_handler import GameEventHandler


class GameLogicWorker(QueueWorker):

    def initialize(self):
        game_handler = GameEventHandler().get()
        self.events_processor = EventsProcessor(
            [game_handler, EventHandler()]  # Regular events and in game events
        )

    def process_event(self, event):
        if not isinstance(event, InGameEvent):
            if event is not None and not isinstance(event, InGameEvent):
                self.events_processor.handle(event)
        else:
            current_screen = CurrentScreen().get_current_screen()
            if current_screen is not None:
                current_screen.update_events(event)
