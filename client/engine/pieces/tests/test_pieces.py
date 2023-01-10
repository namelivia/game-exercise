from unittest import TestCase
from client.engine.general_state.queue import Queue
from client.engine.event_handler import EventHandler
from client.engine.pieces.commands import PlaceASymbol
from client.engine.pieces.events import PlaceASymbolNetworkRequestEvent
from common.messages import PlaceASymbolMessage
import mock


class TestPieces(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.profile.game_id = "game_id"
        self.profile.id = "player_id"
        self.queue = Queue()
        self.event_handler = EventHandler()

    @mock.patch("client.engine.event_handler.Channel.send_command")
    def test_requesting_placing_a_symbol(self, m_send_command):
        # The command is invoked whith a new symbol placement
        PlaceASymbol(self.profile, self.queue, "game_id", "event_id", 2).execute()

        # The PlaceASymbol command creates a PlaceASymbolNetworkRequestEvent
        network_event = self.queue.pop()
        assert isinstance(network_event, PlaceASymbolNetworkRequestEvent)

        # And network request to ask for setting the message on the server is sent
        client_state = mock.Mock()
        client_state.profile = self.profile
        self.event_handler.handle(network_event, client_state)

        # Assert the payload has been correctly sent.
        m_send_command.assert_called_once()
        request_message = m_send_command.call_args.args[0]
        assert isinstance(request_message, PlaceASymbolMessage)
        assert request_message.game_id == "game_id"
        assert request_message.event_id == "event_id"
        assert request_message.player_id == "player_id"
        assert request_message.position == 2
