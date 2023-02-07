from unittest import TestCase

import mock

from client.engine.primitives.event import InGameEvent
from client.engine.screen_manager import ScreenManager


class TestScreenManager(TestCase):
    def setUp(self):
        self.client_state = mock.Mock()
        self.input_manager = mock.Mock()
        self.graphics = mock.Mock()
        self.screen_manager = ScreenManager(
            self.client_state, self.input_manager, self.graphics
        )

    @mock.patch(
        "client.engine.screen_manager.ServerPolling.push_polling_event_if_needed"
    )
    @mock.patch("client.engine.screen_manager.UserInput.process")
    def test_main_loop_iteration(self, m_process_input, m_push_polling_event):
        self.client_state.clock.get.return_value = 120
        event = mock.Mock(InGameEvent)
        self.client_state.queue.pop.return_value = event  # Event from the queue
        current_screen = mock.Mock()
        self.client_state.get_current_screen.return_value = current_screen
        self.input_manager.read.return_value = []  # no input

        # Run one iteration
        self.screen_manager.run()

        # The clock value was incremented.
        self.client_state.clock.tick.assert_called_once_with()

        # A polling request is made if needed
        m_push_polling_event.assert_called_once_with(self.client_state)

        # The latest event from queue is retrieved and processed
        # TODO: This assertion is missing

        # The screen is redrawn
        self.graphics.render.assert_called_once_with(current_screen)

        # The user input is read
        m_process_input.assert_called_once_with(self.input_manager, self.client_state)

        # The screen is updated
        current_screen.update.assert_called_once_with(
            event  # The screen receives the ingame event
        )
