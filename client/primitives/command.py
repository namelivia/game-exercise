from abc import ABC


class Command(ABC):

    def __init__(self, profile, queue, description):
        self.description = description
        self.profile = profile
        self.queue = queue
        self.events = []

    def execute(self):
        for event in self.events:
            self.queue.put(event)
