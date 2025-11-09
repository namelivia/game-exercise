from engine.current_screen import CurrentScreen
from engine.primitives.event import InGameEvent
from engine.threading.queue_worker import QueueWorker

from .event_handler import EventHandler
from .events_processor import EventsProcessor
from .game_event_handler import GameEventHandler


class GameLogicWorker(QueueWorker):

    def initialize(self):
        game_handler = GameEventHandler().get()  # Game event handler
        handlers = [game_handler] if game_handler is not None else []
        handlers.append(EventHandler())  # Game engine event handler
        self.events_processor = EventsProcessor(handlers)

    def process_event(self, event):
        if not isinstance(event, InGameEvent):
            if event is not None and not isinstance(event, InGameEvent):
                self.events_processor.handle(event)
        else:
            current_screen = CurrentScreen().get_current_screen()
            if current_screen is not None:
                current_screen.update_events(event)
