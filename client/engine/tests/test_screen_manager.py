from unittest import TestCase

import mock

from client.engine.primitives.event import InGameEvent
from client.engine.screen_manager import ScreenManager


class TestScreenManager(TestCase):
    def setUp(self):
        self.keyboard_input = mock.Mock()
        self.mouse_input = mock.Mock()
        self.graphics = mock.Mock()
        self.event_handler = mock.Mock()
        self.screen_manager = ScreenManager(
            self.keyboard_input,
            self.mouse_input,
            self.graphics,
            self.event_handler,
        )

    @mock.patch(
        "client.engine.screen_manager.ServerPolling.push_polling_event_if_needed"
    )
    @mock.patch("client.engine.screen_manager.UserInput.process")
    def test_main_loop_iteration(self, m_process_input, m_push_polling_event):
        # clock.get.return_value = 120
        event = mock.Mock(InGameEvent)
        # queue.pop.return_value = event  # Event from the queue
        current_screen = mock.Mock()
        # get_current_screen.return_value = current_screen
        self.keyboard_input.read.return_value = []  # no input
        self.mouse_input.read.return_value = None  # no input

        # Run one iteration
        self.screen_manager.run()

        # A polling request is made if needed
        m_push_polling_event.assert_called_once()

        # The latest event from queue is retrieved and processed
        # TODO: This assertion is missing

        # The screen is redrawn
        self.graphics.render.assert_called_once_with(current_screen)

        # The user input is read
        m_process_input.assert_called_once_with(self.keyboard_input, self.mouse_input)

        # The screen is updated
        current_screen.update.assert_called_once_with(
            event  # The screen receives the ingame event
        )
