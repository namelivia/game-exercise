from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.engine.primitives.event import Event
    from client.engine.general_state.client_state import ClientState


class EventHandler(ABC):
    def handle(self, event: "Event", client_state: "ClientState") -> None:
        pass
