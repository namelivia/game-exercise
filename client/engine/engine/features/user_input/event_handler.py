from typing import TYPE_CHECKING, Any, Dict, Type

from engine.primitives.event_handler import EventHandler

from .events import DisableUserInputEvent
from .state import State

if TYPE_CHECKING:
    from engine.primitives.event import Event


class DisableUserInputEventHandler(EventHandler[DisableUserInputEvent]):
    def handle(self, event: DisableUserInputEvent) -> None:
        State().disable()


handlers_map: Dict[Type["Event"], Any] = {
    DisableUserInputEvent: DisableUserInputEventHandler
}
