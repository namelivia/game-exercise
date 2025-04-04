from unittest import TestCase

import mock

from client.engine.general_state.queue import Queue
from client.engine.visual_regression.visual_regression import VisualRegression
from client.experiment.screens.main.main import MainScreen


class TestMainScreen(TestCase):
    def _initialize_test_queue(self):
        Queue().initialize(None)

    def setUp(self):
        self._initialize_test_queue()
        self.main = MainScreen()

    @mock.patch(
        "client.engine.external.foundational_wrapper.FoundationalWrapper.get_mouse_position"
    )
    def test_visual_regression(self, m_get_mouse_position):
        m_get_mouse_position.return_value = [0, 0]
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
