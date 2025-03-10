from unittest import TestCase

import mock

from client.engine.general_state.profile.profile import Profile
from client.engine.general_state.profile_manager import ProfileManager
from client.engine.server_polling import ServerPolling


class TestServerPolling(TestCase):

    @mock.patch("client.engine.server_polling.RequestGameStatus")
    @mock.patch("client.engine.general_state.profile_manager.Persistence")
    def test_no_polling_if_not_in_a_game(self, m_persistence, m_polling_command):
        m_persistence.load.return_value = Profile(
            key="test_profile",
            id="player_id",
            game_id=None,
            game_event_pointer=None,
        )
        ProfileManager().set_profile("test_profile")
        ServerPolling.push_polling_event_if_needed()
        m_polling_command.assert_not_called()

    @mock.patch("client.engine.server_polling.RequestGameStatus")
    @mock.patch("client.engine.server_polling.ServerPolling._get_polling_rate")
    @mock.patch("client.engine.general_state.profile_manager.Persistence")
    def test_no_polling_if_not_polling_time(
        self, m_persistence, m_get_polling_rate, m_polling_command
    ):
        m_get_polling_rate.return_value = 100
        m_persistence.load.return_value = Profile(
            key="test_profile",
            id="player_id",
            game_id="game_id",
            game_event_pointer=None,
        )
        ProfileManager().set_profile("test_profile")
        # clock.get.return_value = 150
        ServerPolling.push_polling_event_if_needed()
        m_polling_command.assert_not_called()

    @mock.patch("client.engine.server_polling.RequestGameStatus")
    @mock.patch("client.engine.server_polling.ServerPolling._get_polling_rate")
    @mock.patch("client.engine.general_state.profile_manager.Persistence")
    def test_requesting_server_polling(
        self, m_persistence, m_get_polling_rate, m_polling_command
    ):
        m_get_polling_rate.return_value = 100
        m_persistence.load.return_value = Profile(
            key="test_profile",
            id="player_id",
            game_id="game_id",
            game_event_pointer=5,
        )
        ProfileManager().set_profile("test_profile")
        # clock.get.return_value = 300
        ServerPolling.push_polling_event_if_needed()
        m_polling_command.assert_called_once_with("game_id", 5)
