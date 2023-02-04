from typing import Any, Optional, TYPE_CHECKING
from queue import SimpleQueue, Empty
import logging

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class Queue:
    def __init__(self) -> None:
        self.data: SimpleQueue["Event"] = SimpleQueue()

    def put(self, new_data: Any) -> None:
        self.data.put(new_data)

    def empty(self) -> bool:
        return self.data.empty()

    def pop(self) -> Optional["Event"]:

        try:
            # This is a sync queue because block is False
            event = self.data.get(block=False)
            logger.info(f"[Event] {event.__class__.__name__}")
            return event
        except Empty:
            return None
