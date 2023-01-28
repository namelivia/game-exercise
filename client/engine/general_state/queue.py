from typing import Any, Optional
from queue import SimpleQueue, Empty
import logging

logger = logging.getLogger(__name__)


class Queue:
    def __init__(self) -> None:
        self.data: "SimpleQueue" = SimpleQueue()

    def put(self, new_data: Any) -> None:
        self.data.put(new_data)

    def empty(self) -> bool:
        return self.data.empty()

    def pop(self) -> Optional[Any]:
        try:
            # This is a sync queue because block is False
            event = self.data.get(block=False)
            logger.info(f"[Event] {event.__class__.__name__}")
            return event
        except Empty:
            return None
