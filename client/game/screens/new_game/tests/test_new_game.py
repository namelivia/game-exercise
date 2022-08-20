from unittest import TestCase
from client.game.screens.new_game.new_game import NewGame
from client.engine.events import UserTypedEvent
from client.engine.visual_regression.visual_regression import VisualRegression
import mock


class TestNewGame(TestCase):
    def setUp(self):
        self.client_state = mock.Mock()
        self.client_state.clock.get.return_value = 0  # Initial time is 0
        self.new_game = NewGame(self.client_state)

    @mock.patch("client.engine.commands.RequestGameCreation")
    def test_new_game_screen(self, m_request_game_creation):

        # Empty screen
        VisualRegression.assert_matches_snapshot(
            self.new_game,
            "./client/game/screens/new_game/tests/screenshots/new_game_no_input.png",
        )

        # User types the word test
        self.new_game.update(
            UserTypedEvent("t"),
        )
        self.new_game.update(
            UserTypedEvent("e"),
        )
        self.new_game.update(
            UserTypedEvent("s"),
        )
        self.new_game.update(
            UserTypedEvent("t"),
        )

        # Typo
        self.new_game.update(
            UserTypedEvent("z"),
        )
        # Deleting last letter
        self.new_game.update(
            UserTypedEvent("backspace"),
        )

        VisualRegression.assert_matches_snapshot(
            self.new_game,
            "./client/game/screens/new_game/tests/screenshots/new_game_test_input.png",
        )

        # User presses enter and creates the new game
        self.new_game.update(
            UserTypedEvent("return"),
        )
        m_request_game_creation.assert_called_once_with(mock.ANY, mock.ANY, "test")
