import logging
from queue import Empty, SimpleQueue
from typing import TYPE_CHECKING, Any, Optional, Type

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class Queue:
    _instance = None

    # This class is a singleton
    def __new__(cls: Type["Queue"], *args: Any, **kwargs: Any) -> "Queue":
        if not cls._instance:
            cls._instance = super(Queue, cls).__new__(cls)
        return cls._instance

    def initialize(self, initial_event: "Event") -> None:
        self.simple_queue: SimpleQueue["Event"] = SimpleQueue()
        if initial_event:
            self.simple_queue.put(initial_event)

    def put(self, new_event: "Event") -> None:
        self.simple_queue.put(new_event)

    def empty(self) -> bool:
        return self.simple_queue.empty()

    def pop(self) -> Optional["Event"]:
        try:
            # This is a sync queue because block is False
            event = self.simple_queue.get(block=False)
            logger.info(f"[Event] {event.__class__.__name__}")
            return event
        except Empty:
            return None
