from unittest import TestCase
from client.engine.server_polling import ServerPolling
import mock


class TestServerPolling(TestCase):
    def setUp(self):
        self.client_state = mock.Mock()

    @mock.patch("client.engine.server_polling.RequestGameStatus")
    def test_no_polling_if_not_in_a_game(self, m_polling_command):
        self.client_state.profile.game_id = None
        ServerPolling.push_polling_event_if_needed(self.client_state)
        m_polling_command.assert_not_called()

    @mock.patch("client.engine.server_polling.RequestGameStatus")
    @mock.patch("client.engine.server_polling.ServerPolling._get_polling_rate")
    def test_no_polling_if_not_polling_time(
        self, m_get_polling_rate, m_polling_command
    ):
        m_get_polling_rate.return_value = 100
        self.client_state.profile.game_id = "game_id"
        self.client_state.clock.get.return_value = 150
        ServerPolling.push_polling_event_if_needed(self.client_state)
        m_polling_command.assert_not_called()

    @mock.patch("client.engine.server_polling.RequestGameStatus")
    @mock.patch("client.engine.server_polling.ServerPolling._get_polling_rate")
    def test_requesting_server_polling(self, m_get_polling_rate, m_polling_command):
        self.client_state.profile = mock.Mock()
        self.client_state.queue = mock.Mock()
        m_get_polling_rate.return_value = 100
        self.client_state.profile.game_id = "game_id"
        self.client_state.profile.game_event_pointer = 5
        self.client_state.clock.get.return_value = 300
        ServerPolling.push_polling_event_if_needed(self.client_state)
        m_polling_command.assert_called_once_with(
            self.client_state.profile, self.client_state.queue, "game_id", 5
        )
