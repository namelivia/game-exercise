from unittest import TestCase
from client.engine.general_state.queue import Queue
from client.engine.event_handler import EventHandler
from client.engine.features.pieces.commands import PlaceASymbol
from client.engine.features.pieces.events import PlaceASymbolNetworkRequestEvent
from common.messages import (
    PlaceASymbolMessage,
    SymbolPlacedConfirmation,
    ErrorMessage,
)
import mock


class TestPieces(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.profile.game_id = "game_id"
        self.profile.id = "player_id"
        self.queue = Queue()
        self.event_handler = EventHandler()

    @mock.patch("client.engine.event_handler.Channel.send_command")
    @mock.patch(
        "client.engine.features.pieces.event_handler.SymbolPlacedConfirmedCommand"
    )
    def test_requesting_placing_a_symbol_success(
        self, m_piece_placed_confirmed, m_send_command
    ):
        # The command is invoked whith a new symbol placement
        PlaceASymbol(self.profile, self.queue, "game_id", "event_id", 2).execute()

        # The PlaceASymbol command creates a PlaceASymbolNetworkRequestEvent
        network_event = self.queue.pop()
        assert isinstance(network_event, PlaceASymbolNetworkRequestEvent)

        # And network request to ask for setting the message on the server is sent
        client_state = mock.Mock()
        client_state.queue = self.queue
        client_state.profile = self.profile

        # The response will be sucessful
        m_send_command.return_value = SymbolPlacedConfirmation("event_id")
        self.event_handler.handle(network_event, client_state)

        # Assert the payload has been correctly sent.
        m_send_command.assert_called_once()
        request_message = m_send_command.call_args.args[0]
        assert isinstance(request_message, PlaceASymbolMessage)
        assert request_message.game_id == "game_id"
        assert request_message.event_id == "event_id"
        assert request_message.player_id == "player_id"
        assert request_message.position == 2

        # Assert that the confirmation command gets called
        m_piece_placed_confirmed.assert_called_once_with(
            self.profile, self.queue, "event_id"
        )

    @mock.patch("client.engine.event_handler.Channel.send_command")
    def test_requesting_placing_a_symbol_error_response(self, m_send_command):
        # The command is invoked whith a new symbol placement
        PlaceASymbol(self.profile, self.queue, "game_id", "event_id", 2).execute()

        # The PlaceASymbol command creates a PlaceASymbolNetworkRequestEvent
        network_event = self.queue.pop()
        assert isinstance(network_event, PlaceASymbolNetworkRequestEvent)

        # And network request to ask for setting the message on the server is sent
        client_state = mock.Mock()
        client_state.profile = self.profile

        # The response won't be sucessful
        m_send_command.return_value = ErrorMessage("Error message")
        self.event_handler.handle(network_event, client_state)

        # Assert the payload has been correctly sent.
        m_send_command.assert_called_once()
        request_message = m_send_command.call_args.args[0]
        assert isinstance(request_message, PlaceASymbolMessage)
        assert request_message.game_id == "game_id"
        assert request_message.event_id == "event_id"
        assert request_message.player_id == "player_id"
        assert request_message.position == 2
        # TODO: Check the error was properly dealt with

    @mock.patch("client.engine.event_handler.Channel.send_command")
    def test_requesting_placing_a_symbol_no_response(self, m_send_command):
        # The command is invoked whith a new symbol placement
        PlaceASymbol(self.profile, self.queue, "game_id", "event_id", 2).execute()

        # The PlaceASymbol command creates a PlaceASymbolNetworkRequestEvent
        network_event = self.queue.pop()
        assert isinstance(network_event, PlaceASymbolNetworkRequestEvent)

        # And network request to ask for setting the message on the server is sent
        client_state = mock.Mock()
        client_state.profile = self.profile

        # The response won't be sucessful
        m_send_command.return_value = None
        self.event_handler.handle(network_event, client_state)

        # Assert the payload has been correctly sent.
        m_send_command.assert_called_once()
        request_message = m_send_command.call_args.args[0]
        assert isinstance(request_message, PlaceASymbolMessage)
        assert request_message.game_id == "game_id"
        assert request_message.event_id == "event_id"
        assert request_message.player_id == "player_id"
        assert request_message.position == 2
        # TODO: Check the error was properly dealt with
