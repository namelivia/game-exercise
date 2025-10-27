from client.engine.features.network.event_handler import handlers_map
from client.engine.threading.queue_worker import QueueWorker


class NetworkWorker(QueueWorker):

    def process_event(self, event):
        handlers_map[type(event)]().handle(event)
