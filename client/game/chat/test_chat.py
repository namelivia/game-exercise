from unittest import TestCase
from .commands import RequestSendChat
from .events import (
    SendChatRequestEvent,
    SendChatNetworkRequestEvent,
)
import mock
from client.engine.general_state.queue import Queue
from client.game.event_handler import EventHandler


class TestChat(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.queue = Queue()
        self.event_handler = EventHandler()

    @mock.patch("client.engine.event_handler.Channel.send_command")
    def test_sending_a_chat_message(self, m_send_command):
        # When there are new events to process these will be pushed to the queue
        message = "This is a test message"
        RequestSendChat(self.profile, self.queue, message).execute()
        event = (
            self.queue.pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, SendChatRequestEvent)

        client_state = mock.Mock()  # TODO: I don't like I have to define this
        client_state.queue = self.queue
        self.event_handler.handle(event, client_state)

        # A network request to ask for setting the message on the server is sent
        event = self.queue.pop()
        assert isinstance(event, SendChatNetworkRequestEvent)
        self.event_handler.handle(event, client_state)

        # Assert the command has been correctly sent. To test the data payload that piece of code should be refactored
        m_send_command.assert_called_once()
