from abc import ABC
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState
    from client.engine.primitives.event import Event


E = TypeVar("E", bound="Event")


class EventHandler(Generic[E], ABC):
    def handle(self, event: E, client_state: "ClientState") -> None:
        pass
