from unittest import TestCase

import mock

from client.engine.visual_regression.visual_regression import VisualRegression
from client.game.screens.options.options import Options


class TestOptions(TestCase):
    def setUp(self):
        self.client_state = mock.Mock()
        self.client_state.clock.get.return_value = 0  # Initial time is 0
        self.options = Options()

    def test_visual_regression(self):
        VisualRegression.assert_matches_snapshot(
            self.options, "./client/game/screens/options/tests/screenshots/options.png"
        )
