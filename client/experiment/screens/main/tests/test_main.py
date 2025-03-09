from unittest import TestCase

import mock

from client.engine.visual_regression.visual_regression import VisualRegression
from client.experiment.screens.main.main import MainScreen


class TestMainScreen(TestCase):
    def setUp(self):
        # self.clock.get.return_value = 0  # Initial time is 0
        # self.mouse.get.return_value = [0, 0]  # Mouse is at 0, 0
        self.main = MainScreen()

    def test_visual_regression(self):
        self.main.update()
        VisualRegression.assert_matches_snapshot(
            self.main,
            "./client/experiment/screens/main/tests/screenshots/main_timestamp_0.png",
        )

        # self.clock.get.return_value = 5500  # Advance to 5500
        self.main.update()
        VisualRegression.assert_matches_snapshot(
            self.main,
            "./client/experiment/screens/main/tests/screenshots/main_timestamp_5500.png",
        )
