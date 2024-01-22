from unittest import TestCase

import mock

from client.engine.user_input import UserInput


class TestUserInput(TestCase):
    def setUp(self):
        self.client_state = mock.Mock()
        self.keyboard_input = mock.Mock()
        self.mouse_input = mock.Mock()

    @mock.patch("pygame.event.get")
    @mock.patch("client.engine.user_input.UserClicked")
    @mock.patch("client.engine.user_input.UserTyped")
    def test_no_user_events(
        self, m_user_typed_command, m_user_clicked_command, m_pygame_event_get
    ):
        self.keyboard_input.read.return_value = []
        self.mouse_input.read.return_value = None
        UserInput.process(self.keyboard_input, self.mouse_input, self.client_state)
        m_user_typed_command.assert_not_called()
        m_user_clicked_command.assert_not_called()

    @mock.patch("pygame.event.get")
    @mock.patch("client.engine.user_input.UserClicked")
    @mock.patch("client.engine.user_input.UserTyped")
    def test_some_user_events(
        self, m_user_typed_command, m_user_clicked_command, m_pygame_event_get
    ):
        self.keyboard_input.read.return_value = ["a", "x", "c"]
        self.mouse_input.read.return_value = "click"
        self.client_state.profile = mock.Mock()
        self.client_state.queue = mock.Mock()
        UserInput.process(self.keyboard_input, self.mouse_input, self.client_state)
        assert m_user_typed_command.call_count == 3
        assert m_user_typed_command.call_args_list == [
            mock.call(self.client_state.profile, self.client_state.queue, "a"),
            mock.call(self.client_state.profile, self.client_state.queue, "x"),
            mock.call(self.client_state.profile, self.client_state.queue, "c"),
        ]
        m_user_clicked_command.assert_called_once_with(
            self.client_state.profile, self.client_state.queue
        )
