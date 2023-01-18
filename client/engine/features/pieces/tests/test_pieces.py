from unittest import TestCase
from client.engine.general_state.queue import Queue
from client.engine.event_handler import EventHandler
from client.engine.features.pieces.commands import (
    PlaceASymbol,
    SymbolPlacedConfirmedCommand,
    SymbolPlacedErroredCommand,
    PlayerPlacedSymbolInGameCommand,
)
from client.engine.features.pieces.events import (
    PlaceASymbolNetworkRequestEvent,
    SymbolPlacedConfirmedInGameEvent,
    PlayerPlacedSymbolInGameEvent,
    SymbolPlacedErroredEvent,
)
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
    @mock.patch(
        "client.engine.features.pieces.event_handler.SymbolPlacedErroredCommand"
    )
    def test_requesting_placing_a_symbol_error_response(self, m_error, m_send_command):
        # The command is invoked whith a new symbol placement
        PlaceASymbol(self.profile, self.queue, "game_id", "event_id", 2).execute()

        # The PlaceASymbol command creates a PlaceASymbolNetworkRequestEvent
        network_event = self.queue.pop()
        assert isinstance(network_event, PlaceASymbolNetworkRequestEvent)

        # And network request to ask for setting the message on the server is sent
        client_state = mock.Mock()
        client_state.queue = self.queue
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

        m_error.assert_called_once_with(self.profile, self.queue, "event_id")

    @mock.patch("client.engine.event_handler.Channel.send_command")
    @mock.patch(
        "client.engine.features.pieces.event_handler.SymbolPlacedErroredCommand"
    )
    def test_requesting_placing_a_symbol_no_response(self, m_error, m_send_command):
        # The command is invoked whith a new symbol placement
        PlaceASymbol(self.profile, self.queue, "game_id", "event_id", 2).execute()

        # The PlaceASymbol command creates a PlaceASymbolNetworkRequestEvent
        network_event = self.queue.pop()
        assert isinstance(network_event, PlaceASymbolNetworkRequestEvent)

        # And network request to ask for setting the message on the server is sent
        client_state = mock.Mock()
        client_state.queue = self.queue
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

        m_error.assert_called_once_with(self.profile, self.queue, "event_id")

    def test_confirm_a_symbol_has_been_placed(self):
        # The command is invoked confirming the symbol placement
        SymbolPlacedConfirmedCommand(self.profile, self.queue, "event_id").execute()

        # The command creates an ingame event
        in_game_confirm_event = self.queue.pop()
        assert isinstance(in_game_confirm_event, SymbolPlacedConfirmedInGameEvent)
        in_game_confirm_event.event_id = "event_id"

    def test_error_when_a_symbol_has_been_placed(self):
        # The command is invoked signaling something went wrong
        SymbolPlacedErroredCommand(self.profile, self.queue, "event_id").execute()

        # The command creates an ingame event
        in_game_error_event = self.queue.pop()
        assert isinstance(in_game_error_event, SymbolPlacedErroredEvent)
        in_game_error_event.event_id = "event_id"

    def test_adding_an_incoming_symbol_placed(self):
        # Let the game know there is a new chat symbol placed
        PlayerPlacedSymbolInGameCommand(
            self.profile, self.queue, "event_id", "player_1", "Hello"
        ).execute()

        # The command creates an ingame event
        in_game_event = self.queue.pop()
        assert isinstance(in_game_event, PlayerPlacedSymbolInGameEvent)
        in_game_event.event_id = "event_id"
        in_game_event.player_id = "player_1"
        in_game_event.message = "hello"
        in_game_event.confirmation = "OK"  # Incoming messages are always confirmed
