from unittest import TestCase

import mock

from client.engine.features.user_input.events import UserTypedEvent
from client.engine.visual_regression.visual_regression import VisualRegression
from client.game.screens.enter_name.enter_name import EnterName


class TestEnterName(TestCase):
    def setUp(self):
        # self.clock.get.return_value = 0  # Initial time is 0
        self.enter_name = EnterName()

    @mock.patch("client.engine.commands.SetPlayerName")
    def test_enter_name_screen(self, m_set_player_name):
        # Empty screen
        VisualRegression.assert_matches_snapshot(
            self.enter_name,
            "./client/game/screens/enter_name/tests/screenshots/enter_name_no_input.png",
        )

        # User types the word test
        self.enter_name.update(
            UserTypedEvent("t"),
        )
        self.enter_name.update(
            UserTypedEvent("e"),
        )
        self.enter_name.update(
            UserTypedEvent("s"),
        )
        self.enter_name.update(
            UserTypedEvent("t"),
        )

        # Typo
        self.enter_name.update(
            UserTypedEvent("z"),
        )
        # Deleting last letter
        self.enter_name.update(
            UserTypedEvent("backspace"),
        )

        VisualRegression.assert_matches_snapshot(
            self.enter_name,
            "./client/game/screens/enter_name/tests/screenshots/enter_name_test_input.png",
        )

        # User presses enter and creates the new game
        self.enter_name.update(
            UserTypedEvent("return"),
        )
        m_set_player_name.assert_called_once_with(mock.ANY, mock.ANY, "test")
