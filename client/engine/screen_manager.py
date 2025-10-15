import sys
from typing import TYPE_CHECKING, Any

from client.engine.backend.backend import Backend
from client.engine.event_handler import EventHandler
from client.engine.general_state.current_screen import CurrentScreen
from client.engine.general_state.queue import QueueManager
from client.engine.threads import ThreadManager

from .events_processor import EventsProcessor

if TYPE_CHECKING:
    from client.engine.primitives.event import Event


class ScreenManagerFactory:
    @staticmethod
    def create(
        *,
        initial_event: "Event",
        game_event_handler: Any,
    ) -> "ScreenManager":
        QueueManager().initialize(initial_event)
        CurrentScreen().initialize()
        ThreadManager().initialize()

        return ScreenManager(
            game_event_handler,
        )


class ScreenManager:
    def __init__(
        self,
        game_event_handler: Any,
    ):
        self.events_processor = EventsProcessor(
            [game_event_handler, EventHandler()]  # Regular events and in game events
        )

    # Main loop
    def run(self) -> None:
        try:
            current_screen = CurrentScreen().get_current_screen()
            if current_screen is not None:
                current_screen.update()

        except KeyboardInterrupt:
            ThreadManager().shutdown()
            Backend.quit()
            sys.exit()
