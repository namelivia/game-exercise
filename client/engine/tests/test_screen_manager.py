from unittest import TestCase
from client.engine.screen_manager import ScreenManager
import mock


class TestScreenManager(TestCase):
    def setUp(self):
        self.client_state = mock.Mock()
        self.input_manager = mock.Mock()
        self.graphics = mock.Mock()
        self.screen_manager = ScreenManager(
            self.client_state, self.input_manager, self.graphics
        )

    def test_main_loop_iteration(self):
        # TODO: This test is not considering polling or user input
        self.client_state.clock.get.return_value = 120
        self.client_state.queue.pop.return_value = "some_event"  # Event from the queue
        current_screen = mock.Mock()
        self.client_state.get_current_screen.return_value = current_screen
        self.input_manager.read.return_value = []  # no input

        self.screen_manager.run()

        self.client_state.clock.tick.assert_called_once_with()  # Clock advances
        self.graphics.render.assert_called_once_with(
            current_screen
        )  # Current screen is drawn
        current_screen.update.assert_called_once_with(
            "some_event"
        )  # Current screen is updated getting the event from the queue
