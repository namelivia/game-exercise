from unittest import TestCase

import mock

from client.engine.features.user_input.events import UserTypedEvent
from client.engine.general_state.queue import QueueManager
from client.engine.visual_regression.visual_regression import VisualRegression
from client.game.screens.new_game.new_game import NewGame


class TestNewGame(TestCase):
    def _initialize_test_queue(self):
        QueueManager().initialize(None)

    def setUp(self):
        self._initialize_test_queue()
        self.new_game = NewGame()

    @mock.patch("client.game.screens.new_game.new_game.RequestGameCreation")
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
        m_request_game_creation.assert_called_once_with("test")
