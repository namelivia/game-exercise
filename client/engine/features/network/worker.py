import threading
from queue import Empty

from client.engine.features.network.event_handler import handlers_map
from client.engine.primitives.event import StopThreadEvent


class StopThread(Exception):
    """Exception raised to signal a thread to stop processing."""

    pass


class NetworkWorker(threading.Thread):

    def __init__(self, name, queue):
        super().__init__()
        self.name = name
        self.queue = queue
        # Log that the worked has started?

    def run(self):
        """The main execution loop for the thread."""
        print(f"[{self.name}] Thread started, waiting for events...")
        while True:
            try:
                event = self.queue.get_for_workers()
                if type(event) is StopThreadEvent:
                    break
                else:
                    handlers_map[type(event)]().handle(event)
            except Empty:
                continue
        print(f"[{self.name}] Thread successfully terminated and exited run().")

    def stop(self):
        self.queue.put(StopThreadEvent())
