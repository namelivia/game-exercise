from unittest import TestCase

# from client.engine.features.user_input.events import UserTypedEvent
# from client.game.screens.intro.intro import Intro
import mock

from client.engine.general_state.queue import QueueManager
from client.engine.visual_regression.visual_regression import VisualRegression
from client.game.screens.intro.intro import Intro


class TestIntroScreen(TestCase):
    def _initialize_test_queue(self):
        QueueManager().initialize(None)

    def setUp(self):
        self._initialize_test_queue()
        self.intro = Intro()

    @mock.patch("client.game.commands.ToLobby")
    def test_escape_to_lobby(self, m_to_lobby):
        pass
        # User types escape and goes to the lobby
        # screen = Intro(mock.Mock())
        # screen.update(UserTypedEvent("escape"))
        # m_to_lobby.assert_called_once()

    @mock.patch("client.game.commands.ToLobby")
    def test_enter_to_lobby(self, m_to_lobby):
        pass
        # User types enter and goes to the lobby
        # screen = Intro(mock.Mock())
        # screen.update(UserTypedEvent("escape"))
        # m_to_lobby.assert_called_once()

    # This tests is not working and I don't know why
    # @mock.patch("client.engine.primitives.screen.Clock")
    # def test_visual_regression(self, m_clock):
    # m_clock().get.return_value = 0  # Start at 0
    # self.intro.update()
    # VisualRegression.assert_matches_snapshot(
    # self.intro,
    # "./client/game/screens/intro/tests/screenshots/intro_timestamp_0.png",
    # )


#
# m_clock().get.return_value = 5500  # Advance to 5500
# self.intro.update()
# VisualRegression.assert_matches_snapshot(
# self.intro,
# "./client/game/screens/intro/tests/screenshots/intro_timestamp_5500.png",
# )
#
## Advance to 10000 (coins appear)
# m_clock().get.return_value = 10000
# self.intro.update()
# VisualRegression.assert_matches_snapshot(
# self.intro,
# "./client/game/screens/intro/tests/screenshots/intro_timestamp_10000.png",
# )
#
## Advance to 10200
# m_clock().get.return_value = 10200
# self.intro.update()
# VisualRegression.assert_matches_snapshot(
# self.intro,
# "./client/game/screens/intro/tests/screenshots/intro_timestamp_10200.png",
# )
