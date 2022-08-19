from unittest import TestCase
from client.game.screens.credits.credits import Credits
from client.visual_regression.visual_regression import VisualRegression
import mock


class TestCredits(TestCase):
    def setUp(self):
        self.client_state = mock.Mock()
        self.client_state.clock.get.return_value = 0  # Initial time is 0
        self.credits = Credits(self.client_state)

    def test_visual_regression(self):
        VisualRegression.assert_matches_snapshot(
            self.credits,
            "./client/game/screens/credits/tests/screenshots/credits.png"
        )
