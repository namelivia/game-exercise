from unittest import TestCase
from client.general_state.queue import Queue
from client.event_handler import EventHandler
from client.events import (
    UserTypedEvent,
    QuitGameEvent
)
from client.commands import (
    QuitGame,
    UserTyped
)
import mock


class TestClient(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.queue = Queue()
        self.event_handler = EventHandler()

    # These are tests for a flow Command => Event => Handler
    @mock.patch("pygame.quit")
    @mock.patch("sys.exit")
    def test_quitting_the_game(self, m_exit, m_pygame_quit):
        QuitGame(self.profile, self.queue).execute()
        event = self.queue.pop()  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, QuitGameEvent)
        client_state = mock.Mock()  # TODO: I don't like I have to define these two
        graphics = mock.Mock()
        self.event_handler.handle(event, client_state, graphics)
        m_pygame_quit.assert_called_once_with()
        m_exit.assert_called_once_with()

    def test_user_typing(self):
        UserTyped(self.profile, self.queue,  "f").execute()
        event = self.queue.pop()  # TODO: Manage the case of commands that queue several events
        assert isinstance(event, UserTypedEvent)
        assert event.key == "f"
        # There is no generic handler for this one, it is handled by the game on each screen
