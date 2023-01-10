from abc import ABC
import logging

logger = logging.getLogger(__name__)


class Command(ABC):
    def __init__(self, profile, queue, description):
        self.description = description
        self.profile = profile
        self.queue = queue
        self.events = []

    def execute(self):
        logger.info(f"[Command] {self.description}")
        for event in self.events:
            self.queue.put(event)
