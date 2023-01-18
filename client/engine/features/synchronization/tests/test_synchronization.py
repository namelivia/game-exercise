from unittest import TestCase
from client.engine.general_state.queue import Queue
from client.engine.event_handler import EventHandler
from client.engine.features.synchronization.commands import (
    RefreshGameStatus,
)
from client.engine.features.synchronization.profile.events import (
    UpdateGameEvent,
)
import mock


class TestSynchronization(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.profile.game_id = "game_id"
        self.profile.id = "player_id"
        self.queue = Queue()
        self.event_handler = EventHandler()

    def test_(self):
        pass
