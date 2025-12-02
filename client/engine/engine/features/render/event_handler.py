from typing import TYPE_CHECKING, Any, Dict, Type

from engine.primitives.event_handler import EventHandler

from .events import RefreshRenderScreenEvent
from .state import State

if TYPE_CHECKING:
    from engine.primitives.event import Event


class RefreshRenderScreenEventHandler(EventHandler[RefreshRenderScreenEvent]):
    def handle(self, event: RefreshRenderScreenEvent) -> None:
        event.screen.load()
        State().set_current_screen(event.screen)


handlers_map: Dict[Type["Event"], Any] = {
    RefreshRenderScreenEvent: RefreshRenderScreenEventHandler
}
