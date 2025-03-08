import logging
from abc import ABC
from typing import TYPE_CHECKING, List

from client.engine.general_state.queue_what import QueueWhat

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class Command(ABC):
    def __init__(self, description: str):
        self.description = description
        self.events: List["Event"] = []

    def execute(self) -> None:
        logger.info(f"[Command] {self.description}")
        queue_what = QueueWhat()
        for event in self.events:
            queue_what.queue.put(event)
