from unittest import TestCase
from client.engine.general_state.queue import Queue
from client.engine.general_state.profile.profile import Profile
from client.engine.event_handler import EventHandler
from .events import ChatMessageInGameEvent
from .commands import ChatMessageInGameCommand
import mock


class TestChat(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.queue = Queue()
        self.event_handler = EventHandler()

    def test_sending_an_ingame_chat_message(self):
        # When there are new events to process these will be pushed to the queue
        profile = Profile(
            key="key",
            id="id",
            game_id="game_id",
            game_event_pointer=0,
            sound_on=False,
        )
        assert profile.name is None
        ChatMessageInGameCommand(
            profile, self.queue, "player_id", "test message"
        ).execute()
        event = (
            self.queue.pop()
        )  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, ChatMessageInGameEvent)
        # Event to be picked up by the game logic
