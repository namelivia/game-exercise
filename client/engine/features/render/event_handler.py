from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.primitives.event_handler import EventHandler

from .events import StartRenderingEvent
from .state import State

if TYPE_CHECKING:
    from client.engine.primitives.event import Event


class StartRenderingEventHandler(EventHandler[StartRenderingEvent]):
    def handle(self, event: StartRenderingEvent) -> None:
        event.screen.load()
        State().set_current_screen(event.screen)


handlers_map: Dict[Type["Event"], Any] = {
    StartRenderingEvent: StartRenderingEventHandler
}
