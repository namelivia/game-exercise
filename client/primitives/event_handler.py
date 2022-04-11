from abc import ABC


class EventHandler(ABC):
    def handle(self, event, client_state, graphics):
        pass
