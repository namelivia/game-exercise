from unittest import TestCase

import mock

from client.engine.user_input import UserInput


class TestUserInput(TestCase):
    def setUp(self):
        self.client_state = mock.Mock()
        self.input_manager = mock.Mock()

    @mock.patch("client.engine.user_input.UserTyped")
    def test_no_user_events(self, m_user_typed_command):
        self.input_manager.read.return_value = []
        UserInput.process(self.input_manager, self.client_state)
        m_user_typed_command.assert_not_called()

    @mock.patch("client.engine.user_input.UserTyped")
    def test_some_user_events(self, m_user_typed_command):
        self.input_manager.read.return_value = ["a", "x", "c"]
        self.client_state.profile = mock.Mock()
        self.client_state.queue = mock.Mock()
        UserInput.process(self.input_manager, self.client_state)
        assert m_user_typed_command.call_count == 3
        assert m_user_typed_command.call_args_list == [
            mock.call(self.client_state.profile, self.client_state.queue, "a"),
            mock.call(self.client_state.profile, self.client_state.queue, "x"),
            mock.call(self.client_state.profile, self.client_state.queue, "c"),
        ]
