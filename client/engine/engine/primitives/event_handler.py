from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from engine.primitives.event import Event


E = TypeVar("E", bound="Event")


class EventHandler(Generic[E], ABC):
    @abstractmethod
    def handle(self, event: E) -> None:
        pass
