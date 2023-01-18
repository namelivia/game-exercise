from unittest import TestCase
from client.game.screens.join_game.join_game import JoinGame
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.visual_regression.visual_regression import VisualRegression
import mock


class TestJoinGame(TestCase):
    def setUp(self):
        self.client_state = mock.Mock()
        self.client_state.clock.get.return_value = 0  # Initial time is 0
        self.join_game = JoinGame(self.client_state)

    @mock.patch("client.game.screens.join_game.join_game.RequestJoiningAGame")
    def test_join_game_screen(self, m_request_join_game):

        # Empty screen
        VisualRegression.assert_matches_snapshot(
            self.join_game,
            "./client/game/screens/join_game/tests/screenshots/join_game_no_input.png",
        )

        # User types the word test
        self.join_game.update(
            UserTypedEvent("t"),
        )
        self.join_game.update(
            UserTypedEvent("e"),
        )
        self.join_game.update(
            UserTypedEvent("s"),
        )
        self.join_game.update(
            UserTypedEvent("t"),
        )

        # Typo
        self.join_game.update(
            UserTypedEvent("z"),
        )
        # Deleting last letter
        self.join_game.update(
            UserTypedEvent("backspace"),
        )

        VisualRegression.assert_matches_snapshot(
            self.join_game,
            "./client/game/screens/join_game/tests/screenshots/join_game_test_input.png",
        )

        # User presses enter and creates the new game
        self.join_game.update(
            UserTypedEvent("return"),
        )
        m_request_join_game.assert_called_once_with(mock.ANY, mock.ANY, "test")
