from typing import TYPE_CHECKING, Any

from engine.clock import Clock
from engine.current_screen import CurrentScreen
from engine.features.game_logic.game_event_handler import GameEventHandler
from engine.queue import QueueManager
from engine.threading.manager import ThreadManager

from .application import Application

if TYPE_CHECKING:
    from engine.primitives.event import Event


def start_application(
    *,
    initial_event: "Event",
    game_event_handler: Any,
) -> "Application":
    Clock().initialize()
    GameEventHandler().set(game_event_handler)
    QueueManager().initialize(initial_event)
    CurrentScreen().initialize()
    ThreadManager().initialize()

    application = Application()
    application.run()
    return application
