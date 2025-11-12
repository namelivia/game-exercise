import threading
import time


class PollingWorker(threading.Thread):

    IDLE_TIME = 0.005

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.stop_event = threading.Event()

    def step(self):
        pass

    def initialize(self):
        pass

    def run(self):
        print(f"[{self.name}] Thread started...")
        self.initialize()
        while not self.stop_event.is_set():
            self.step()
            time.sleep(PollingWorker.IDLE_TIME)

        print(f"[{self.name}] Thread successfully terminated and exited run().")

    def stop(self):
        self.stop_event.set()
