from unittest import TestCase

import mock

from client.engine.event_handler import EventHandler
from client.engine.general_state.queue import QueueManager


class TestGameList(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.profile.game_id = "game_id"
        self.profile.id = "player_id"
        self.queue = QueueManager()
        self.event_handler = EventHandler()

    def test_test(self):
        pass
