import uuid
from typing import TYPE_CHECKING, Any, Type

from .queue import Queue

if TYPE_CHECKING:
    from client.engine.primitives.event import Event


# This is a singleton
class QueueWhat:
    _instance = None

    def __new__(cls: Type["QueueWhat"], *args: Any, **kwargs: Any) -> "QueueWhat":
        if not cls._instance:
            cls._instance = super(QueueWhat, cls).__new__(cls)
        return cls._instance

    def initialize(self, initial_event: "Event") -> None:
        self.queue = Queue()
        self.queue.put(initial_event)
