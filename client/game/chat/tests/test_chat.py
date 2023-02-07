from unittest import TestCase

import mock

from client.engine.features.chat.events import ChatMessageInGameEvent
from client.engine.general_state.queue import Queue
from client.game.chat.commands import RequestSendChat
from client.game.chat.events import SendChatRequestEvent


class TestChat(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.profile.id = "player_id"
        self.queue = Queue()
        self.event_handler = mock.Mock()

    @mock.patch("uuid.uuid4")
    def test_sending_a_chat_message(self, m_uuid):
        # The command is invoked whith a new chat message
        m_uuid.return_value = "event_id"
        RequestSendChat(self.profile, self.queue, "This is a test message").execute()

        # Two events will be created, a request to display the chat
        ingame_event = self.queue.pop()
        assert isinstance(ingame_event, ChatMessageInGameEvent)
        assert ingame_event.player_id == "player_id"
        assert ingame_event.message == "This is a test message"

        # And another event to request the chat delivery
        request_event = self.queue.pop()
        assert isinstance(request_event, SendChatRequestEvent)
        assert request_event.event_id == "event_id"
        assert request_event.message == "This is a test message"
