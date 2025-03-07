from unittest import TestCase

import mock

from client.engine.server_polling import ServerPolling


class TestServerPolling(TestCase):
    @mock.patch("client.engine.server_polling.RequestGameStatus")
    @mock.patch("client.engine.server_polling.ClientState")
    def test_no_polling_if_not_in_a_game(self, m_client_state, m_polling_command):
        m_client_state.profile.game_id = None
        ServerPolling.push_polling_event_if_needed()
        m_polling_command.assert_not_called()

    @mock.patch("client.engine.server_polling.RequestGameStatus")
    @mock.patch("client.engine.server_polling.ServerPolling._get_polling_rate")
    @mock.patch("client.engine.server_polling.ClientState")
    def test_no_polling_if_not_polling_time(
        self, m_client_state, m_get_polling_rate, m_polling_command
    ):
        m_get_polling_rate.return_value = 100
        m_client_state.profile.game_id = "game_id"
        m_client_state.clock.get.return_value = 150
        ServerPolling.push_polling_event_if_needed()
        m_polling_command.assert_not_called()

    @mock.patch("client.engine.server_polling.RequestGameStatus")
    @mock.patch("client.engine.server_polling.ServerPolling._get_polling_rate")
    @mock.patch("client.engine.server_polling.ClientState")
    def test_requesting_server_polling(
        self, m_client_state, m_get_polling_rate, m_polling_command
    ):
        m_client_state.profile = mock.Mock()
        m_client_state.queue = mock.Mock()
        m_get_polling_rate.return_value = 100
        m_client_state().profile.game_id = "game_id"
        m_client_state().profile.game_event_pointer = 5
        m_client_state().clock.get.return_value = 300
        ServerPolling.push_polling_event_if_needed()
        m_polling_command.assert_called_once_with(
            m_client_state().profile, m_client_state().queue, "game_id", 5
        )
