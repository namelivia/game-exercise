import threading

from engine.primitives.event import StopThreadEvent


class QueueWorker(threading.Thread):

    def __init__(self, name, queue):
        super().__init__()
        self.name = name
        self.queue = queue

    def initialize(self):
        pass

    def process_event(self, event):
        pass

    def run(self):
        print(f"[{self.name}] Thread started...")
        self.initialize()
        while True:
            event = self.queue.get()
            if type(event) is StopThreadEvent:
                break
            else:
                self.process_event(event)

        print(f"[{self.name}] Thread successfully terminated and exited run().")

    def stop(self):
        self.queue.put(StopThreadEvent())
