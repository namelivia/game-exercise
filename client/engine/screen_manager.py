import sys
import time
from typing import TYPE_CHECKING, Any, Callable, Optional  # Added Callable and Optional

from client.engine.backend.backend import Backend
from client.engine.clock import Clock
from client.engine.event_handler import EventHandler
from client.engine.features.game_logic.game_event_handler import GameEventHandler
from client.engine.general_state.current_screen import CurrentScreen
from client.engine.general_state.queue import QueueManager
from client.engine.threads import ThreadManager

if TYPE_CHECKING:
    from client.engine.primitives.event import Event
    from client.engine.primitives.screen import Screen


class ScreenManagerFactory:
    @staticmethod
    def create(
        *,
        initial_event: "Event",
        # Assuming game_event_handler is a callable (a function or method) that takes an Event and returns None
        game_event_handler: Callable[["Event"], None],
    ) -> "ScreenManager":
        Clock().initialize()
        GameEventHandler().set(game_event_handler)
        QueueManager().initialize(initial_event)
        CurrentScreen().initialize()
        ThreadManager().initialize()

        return ScreenManager()


class ScreenManager:
    def run(self) -> None:
        current_screen: Optional["Screen"]

        try:
            current_screen = CurrentScreen().get_current_screen()

            if current_screen is not None:
                current_screen.update()

            time.sleep(0.01)

        except KeyboardInterrupt:
            ThreadManager().shutdown()
            Backend.quit()
            sys.exit()
