from unittest import TestCase

import mock

from client.engine.features.pieces.events import PlayerPlacedSymbolInGameEvent
from client.engine.general_state.queue import Queue
from client.game.pieces.commands import RequestPlaceASymbol
from client.game.pieces.events import PlaceASymbolRequestEvent


class TestPieces(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.profile.id = "player_id"
        self.queue = Queue()
        self.event_handler = mock.Mock()

    @mock.patch("uuid.uuid4")
    def test_requesting_placing_a_symbol(self, m_uuid):
        # The command is invoked whith the symbol position
        m_uuid.return_value = "event_id"
        RequestPlaceASymbol(self.profile, self.queue, 2).execute()

        # Two events will be created, a request to display the chat
        ingame_event = self.queue.pop()
        assert isinstance(ingame_event, PlayerPlacedSymbolInGameEvent)
        assert ingame_event.player_id == "player_id"
        assert ingame_event.position == 2

        # And another event to request the position placement delivery
        request_event = self.queue.pop()
        assert isinstance(request_event, PlaceASymbolRequestEvent)
        assert request_event.event_id == "event_id"
        assert request_event.position == 2
