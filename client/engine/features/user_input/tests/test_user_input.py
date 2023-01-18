from unittest import TestCase
from client.engine.general_state.queue import Queue
from client.engine.event_handler import EventHandler
from client.engine.features.user_input.commands import UserTyped
from client.engine.features.user_input.events import UserTypedEvent
import mock


class TestUserInput(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.profile.game_id = "game_id"
        self.profile.id = "player_id"
        self.queue = Queue()
        self.event_handler = EventHandler()

    def test_user_input(self):
        # The command is invoked whith the key the user typed
        UserTyped(self.profile, self.queue, "a").execute()

        # The UserTyped command creates a UserTypedEvent for the screen
        event = self.queue.pop()
        assert isinstance(event, UserTypedEvent)
        assert event.key == "a"
