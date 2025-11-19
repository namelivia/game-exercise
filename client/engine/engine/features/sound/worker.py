from engine.features.sound.event_handler import handlers_map
from engine.threading.queue_worker import QueueWorker

from .backend.pygame.sound import SoundBackend
from .state import State


class SoundWorker(QueueWorker):

    def initialize(self):
        SoundBackend.init()
        State().initialize()

    def process_event(self, event):
        handlers_map[type(event)]().handle(event)
