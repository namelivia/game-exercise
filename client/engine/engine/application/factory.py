from typing import TYPE_CHECKING, Any, Optional, Type

from engine.clock import Clock
from engine.features.game_logic.events import ScreenTransitionEvent
from engine.features.game_logic.game_event_handler import GameEventHandler
from engine.primitives.screen import Screen
from engine.queue import QueueManager
from engine.threading.manager import ThreadManager

from .application import Application


def start_application(
    *,
    initial_screen: Type[Screen],
    game_event_handler: Optional[Any] = None,
) -> "Application":
    Clock().initialize()
    GameEventHandler().initialize()
    if game_event_handler is not None:
        GameEventHandler().set(game_event_handler)
    QueueManager().initialize(ScreenTransitionEvent(initial_screen()))
    ThreadManager().initialize()

    application = Application()
    application.run()
    return application
