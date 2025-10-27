from client.engine.backend.sound import SoundBackend
from client.engine.features.sound.event_handler import handlers_map
from client.engine.threading.queue_worker import QueueWorker


class SoundWorker(QueueWorker):

    def initialize(self):
        SoundBackend.init()

    def process_event(self, event):
        handlers_map[type(event)]().handle(event)
