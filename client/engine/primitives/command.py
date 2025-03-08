import logging
from abc import ABC
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from client.engine.general_state.queue import Queue
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class Command(ABC):
    def __init__(self, queue: "Queue", description: str):
        self.description = description
        self.queue = queue
        self.events: List["Event"] = []

    def execute(self) -> None:
        logger.info(f"[Command] {self.description}")
        for event in self.events:
            self.queue.put(event)
