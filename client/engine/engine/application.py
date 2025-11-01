import sys
import time
from typing import TYPE_CHECKING, Any

from engine.backend.backend import Backend
from engine.clock import Clock
from engine.current_screen import CurrentScreen
from engine.features.game_logic.game_event_handler import GameEventHandler
from engine.queue import QueueManager
from engine.threading.manager import ThreadManager

if TYPE_CHECKING:
    from engine.primitives.event import Event


class ApplicationFactory:
    @staticmethod
    def create(
        *,
        initial_event: "Event",
        game_event_handler: Any,
    ) -> "Application":
        Clock().initialize()
        GameEventHandler().set(game_event_handler)
        QueueManager().initialize(initial_event)
        CurrentScreen().initialize()
        ThreadManager().initialize()

        return Application()


class Application:
    # Main loop
    def run(self) -> None:
        while True:
            try:
                current_screen = CurrentScreen().get_current_screen()
                if current_screen is not None:
                    current_screen.update()
                time.sleep(0.01)

            except KeyboardInterrupt:
                ThreadManager().shutdown()
                Backend.quit()
                sys.exit()
