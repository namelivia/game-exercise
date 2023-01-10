from unittest import TestCase
from client.engine.general_state.queue import Queue
from client.engine.general_state.profile.profile import Profile
from client.engine.event_handler import EventHandler
from client.engine.chat.commands import SendChat
from client.engine.chat.events import SendChatNetworkRequestEvent
from common.messages import SendChatMessage
import mock


class TestChat(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.profile.game_id = "game_id"
        self.profile.id = "player_id"
        self.queue = Queue()
        self.event_handler = EventHandler()

    def test_chat_message_confirmed_command(self):
        # When there are new events to process these will be pushed to the queue
        profile = Profile(
            key="key",
            id="id",
            game_id="game_id",
            game_event_pointer=0,
            sound_on=False,
        )
        assert profile.name is None
        # TODO: Finish writing this test

    def test_chat_message_in_game_command(self):
        # When there are new events to process these will be pushed to the queue
        profile = Profile(
            key="key",
            id="id",
            game_id="game_id",
            game_event_pointer=0,
            sound_on=False,
        )
        assert profile.name is None
        # TODO: Finish writing this test

    def test_chat_message_errored_command(self):
        # When there are new events to process these will be pushed to the queue
        profile = Profile(
            key="key",
            id="id",
            game_id="game_id",
            game_event_pointer=0,
            sound_on=False,
        )
        assert profile.name is None
        # TODO: Finish writing this test

    @mock.patch("client.engine.event_handler.Channel.send_command")
    def test_sending_a_chat_message(self, m_send_command):
        # The command is invoked whith a new chat message
        SendChat(
            self.profile, self.queue, "game_id", "event_id", "This is a test message"
        ).execute()

        # The SendChat command creates a SendChatNetworkRequestEvent
        network_event = self.queue.pop()
        assert isinstance(network_event, SendChatNetworkRequestEvent)

        # And network request to ask for setting the message on the server is sent
        client_state = mock.Mock()
        client_state.profile = self.profile
        self.event_handler.handle(network_event, client_state)

        # Assert the payload has been correctly sent.
        m_send_command.assert_called_once()
        request_message = m_send_command.call_args.args[0]
        assert isinstance(request_message, SendChatMessage)
        assert request_message.game_id == "game_id"
        assert request_message.event_id == "event_id"
        assert request_message.player_id == "player_id"
        assert request_message.message == "This is a test message"
