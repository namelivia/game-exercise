from unittest import TestCase

import mock

from client.engine.features.pieces.events import PlayerPlacedSymbolInGameEvent
from client.engine.general_state.profile.profile import Profile
from client.engine.general_state.profile_manager import ProfileManager
from client.engine.general_state.queue import Queue
from client.game.pieces.commands import RequestPlaceASymbol
from client.game.pieces.events import PlaceASymbolRequestEvent


class TestPieces(TestCase):
    @mock.patch("client.engine.general_state.profile_manager.Persistence")
    def _initialize_test_profile(self, m_persistence):
        m_persistence.load.return_value = Profile(
            key="test_profile",
            id="player_id",
            game_id="game_id",
            game_event_pointer=None,
        )
        ProfileManager().set_profile("test_profile")

    def _initialize_test_queue(self):
        Queue().initialize(None)

    def setUp(self):
        self._initialize_test_queue()
        self.test_profile = self._initialize_test_profile()
        self.event_handler = mock.Mock()

    @mock.patch("uuid.uuid4")
    def test_requesting_placing_a_symbol(self, m_uuid):
        # The command is invoked whith the symbol position
        m_uuid.return_value = "event_id"
        RequestPlaceASymbol(2).execute()

        # Two events will be created, a request to display the chat
        ingame_event = Queue().pop()
        assert isinstance(ingame_event, PlayerPlacedSymbolInGameEvent)
        # assert ingame_event.player_id == self.test_profile.id
        assert ingame_event.position == 2

        # And another event to request the position placement delivery
        request_event = Queue().pop()
        assert isinstance(request_event, PlaceASymbolRequestEvent)
        assert request_event.event_id == "event_id"
        assert request_event.position == 2
