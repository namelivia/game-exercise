import sys
import time
from typing import TYPE_CHECKING, Any

from client.engine.backend.backend import Backend
from client.engine.clock import Clock
from client.engine.event_handler import EventHandler
from client.engine.features.game_logic.game_event_handler import GameEventHandler
from client.engine.general_state.current_screen import CurrentScreen
from client.engine.queue import QueueManager
from client.engine.threading.manager import ThreadManager

if TYPE_CHECKING:
    from client.engine.primitives.event import Event


class ScreenManagerFactory:
    @staticmethod
    def create(
        *,
        initial_event: "Event",
        game_event_handler: Any,
    ) -> "ScreenManager":
        Clock().initialize()
        GameEventHandler().set(game_event_handler)
        QueueManager().initialize(initial_event)
        CurrentScreen().initialize()
        ThreadManager().initialize()

        return ScreenManager()


class ScreenManager:
    # Main loop
    def run(self) -> None:
        try:
            current_screen = CurrentScreen().get_current_screen()
            if current_screen is not None:
                current_screen.update()
            time.sleep(0.01)

        except KeyboardInterrupt:
            ThreadManager().shutdown()
            Backend.quit()
            sys.exit()
