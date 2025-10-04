from typing import TYPE_CHECKING, Any

from client.engine.event_handler import EventHandler
from client.engine.general_state.current_screen import CurrentScreen
from client.engine.general_state.queue import QueueManager
from client.engine.primitives.event import InGameEvent
from client.engine.threads import ThreadManager

from .events_processor import EventsProcessor

if TYPE_CHECKING:
    from client.engine.primitives.event import Event


class ScreenManagerFactory:
    @staticmethod
    def create(
        *,
        initial_event: "Event",
        event_handler: Any,
    ) -> "ScreenManager":
        QueueManager().initialize(initial_event)
        CurrentScreen().initialize()
        ThreadManager().initialize()

        return ScreenManager(
            event_handler,
        )


class ScreenManager:
    def __init__(
        self,
        event_handler: Any,
    ):
        self.events_processor = EventsProcessor(
            [event_handler, EventHandler()]  # Regular events and in game events
        )

    # Main loop
    def run(self) -> None:

        # 2 - Fetch and handle the latest event
        event = QueueManager().main_queue().pop()

        # TODO: I don't like this if
        if event is not None and not isinstance(event, InGameEvent):
            self.events_processor.handle(event)

        current_screen = CurrentScreen().get_current_screen()

        if current_screen is not None:
            # 3 - Update the current screen

            # TODO: I don't like this if
            if not isinstance(event, InGameEvent):
                event = None
            # it is an ingame event
            current_screen.update(event)
