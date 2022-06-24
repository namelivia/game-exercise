from unittest import TestCase
from client.game.commands import RequestPlaceASymbol
from client.game.events import (
    PlaceASymbolRequestEvent,
    PlaceASymbolNetworkRequestEvent,
)
import mock
from client.general_state.queue import Queue
from client.game.event_handler import EventHandler


class TestGame(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.queue = Queue()
        self.event_handler = EventHandler()

    @mock.patch("client.event_handler.Channel.send_command")
    def test_placing_a_symbol(self, m_send_command):
        # When there are new events to process these will be pushed to the queue
        position = 2
        RequestPlaceASymbol(self.profile, self.queue, position).execute()
        event = (
            self.queue.pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, PlaceASymbolRequestEvent)

        client_state = mock.Mock()  # TODO: I don't like I have to define this
        client_state.queue = self.queue
        self.event_handler.handle(event, client_state)

        # A network request to ask for the placing the symbol on the server is sent
        event = self.queue.pop()
        assert isinstance(event, PlaceASymbolNetworkRequestEvent)
        self.event_handler.handle(event, client_state)

        # Assert the command has been correctly sent. To test the data payload that piece of code should be refactored
        m_send_command.assert_called_once()
