from unittest import TestCase

import mock

from client.engine.event_handler import EventHandler
from client.engine.features.chat.commands import (
    ChatMessageConfirmedCommand,
    ChatMessageErroredCommand,
    ChatMessageInGameCommand,
    SendChat,
)
from client.engine.features.chat.events import (
    ChatMessageConfirmedInGameEvent,
    ChatMessageErroredEvent,
    ChatMessageInGameEvent,
    SendChatNetworkRequestEvent,
)
from client.engine.general_state.profile.profile import Profile
from client.engine.general_state.profile_manager import ProfileManager
from client.engine.general_state.queue import QueueManager
from common.messages import ChatMessageConfirmation, ErrorMessage, SendChatMessage


class TestChat(TestCase):
    def _initialize_test_queue(self):
        QueueManager().initialize(None)

    @mock.patch("client.engine.general_state.profile_manager.Persistence")
    def _initialize_test_profile(self, m_persistence):
        m_persistence.load.return_value = Profile(
            key="test_profile",
            id="player_id",
            game_id="game_id",
            game_event_pointer=None,
        )
        ProfileManager().set_profile("test_profile")

    def setUp(self):
        self._initialize_test_queue()
        self._initialize_test_profile()
        self.event_handler = EventHandler()

    @mock.patch("client.engine.event_handler.Channel.send_command")
    @mock.patch("client.engine.features.chat.event_handler.ChatMessageConfirmedCommand")
    def test_sending_a_chat_message_success(
        self, m_chat_message_confirmed, m_send_command
    ):
        # The command is invoked whith a new chat message
        SendChat("game_id", "event_id", "This is a test message").execute()

        # The SendChat command creates a SendChatNetworkRequestEvent
        network_event = QueueManager().main_queue().pop()
        assert isinstance(network_event, SendChatNetworkRequestEvent)

        # The response will be sucessful
        m_send_command.return_value = ChatMessageConfirmation("event_id")
        self.event_handler.handle(network_event)

        # Assert the payload has been correctly sent.
        m_send_command.assert_called_once()
        request_message = m_send_command.call_args.args[0]
        assert isinstance(request_message, SendChatMessage)
        assert request_message.game_id == "game_id"
        assert request_message.event_id == "event_id"
        assert request_message.player_id == "player_id"
        assert request_message.message == "This is a test message"

        # Assert that the confirmation command gets called
        m_chat_message_confirmed.assert_called_once_with("event_id")

    @mock.patch("client.engine.event_handler.Channel.send_command")
    @mock.patch("client.engine.features.chat.event_handler.ChatMessageErroredCommand")
    def test_sending_a_chat_message_error_response(self, m_error, m_send_command):
        # The command is invoked whith a new chat message
        SendChat("game_id", "event_id", "This is a test message").execute()

        # The SendChat command creates a SendChatNetworkRequestEvent
        network_event = QueueManager().main_queue().pop()
        assert isinstance(network_event, SendChatNetworkRequestEvent)

        # The response won't be sucessful
        m_send_command.return_value = ErrorMessage("Error message")
        self.event_handler.handle(network_event)

        # Assert the payload has been correctly sent.
        m_send_command.assert_called_once()
        request_message = m_send_command.call_args.args[0]
        assert isinstance(request_message, SendChatMessage)
        assert request_message.game_id == "game_id"
        assert request_message.event_id == "event_id"
        assert request_message.player_id == "player_id"
        assert request_message.message == "This is a test message"

        m_error.assert_called_once_with("event_id")

    @mock.patch("client.engine.event_handler.Channel.send_command")
    @mock.patch("client.engine.features.chat.event_handler.ChatMessageErroredCommand")
    def test_sending_a_chat_message_no_response(self, m_error, m_send_command):
        # The command is invoked whith a new chat message
        SendChat("game_id", "event_id", "This is a test message").execute()

        # The SendChat command creates a SendChatNetworkRequestEvent
        network_event = QueueManager().main_queue().pop()
        assert isinstance(network_event, SendChatNetworkRequestEvent)

        # The response won't be sucessful
        m_send_command.return_value = None
        self.event_handler.handle(network_event)

        # Assert the payload has been correctly sent.
        m_send_command.assert_called_once()
        request_message = m_send_command.call_args.args[0]
        assert isinstance(request_message, SendChatMessage)
        assert request_message.game_id == "game_id"
        assert request_message.event_id == "event_id"
        assert request_message.player_id == "player_id"
        assert request_message.message == "This is a test message"

        m_error.assert_called_once_with("event_id")

    def test_confirm_a_chat_has_been_posted(self):
        # The command is invoked confirming the chat post
        ChatMessageConfirmedCommand("event_id").execute()

        # The command creates an ingame event
        in_game_confirm_event = QueueManager().main_queue().pop()
        assert isinstance(in_game_confirm_event, ChatMessageConfirmedInGameEvent)
        in_game_confirm_event.event_id = "event_id"

    def test_error_when_a_chat_was_incorrectly_posted(self):
        # The command is invoked signaling something went wrong
        ChatMessageErroredCommand("event_id").execute()

        # The command creates an ingame event
        in_game_error_event = QueueManager().main_queue().pop()
        assert isinstance(in_game_error_event, ChatMessageErroredEvent)
        in_game_error_event.event_id = "event_id"

    def test_adding_an_incoming_chat_message(self):
        # Let the game know there is a new chat message
        ChatMessageInGameCommand("event_id", "player_1", "Hello").execute()

        # The command creates an ingame event
        in_game_event = QueueManager().main_queue().pop()
        assert isinstance(in_game_event, ChatMessageInGameEvent)
        in_game_event.event_id = "event_id"
        in_game_event.player_id = "player_1"
        in_game_event.message = "hello"
        in_game_event.confirmation = "OK"  # Incoming messages are always confirmed
