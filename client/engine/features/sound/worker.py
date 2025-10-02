import threading

from client.engine.features.sound.event_handler import handlers_map


class StopThread(Exception):
    """Exception raised to signal a thread to stop processing."""

    pass


class SoundWorker(threading.Thread):

    def __init__(self, name, queue):
        super().__init__()
        self.name = name
        self.queue = queue
        # Event used to signal the thread to stop gracefully
        self.stop_event = threading.Event()
        # Log that the worked has started?

    def run(self):
        """The main execution loop for the thread."""
        print(f"[{self.name}] Thread started, waiting for events...")
        while not self.stop_event.is_set():
            try:
                if not self.queue.empty():
                    event = self.queue.pop()
                    handlers_map[type(event)]().handle(event)
            except StopThread:
                # Internal exception to cleanly exit the loop
                break
            except Exception as e:
                print(f"Error {e}")
                break
