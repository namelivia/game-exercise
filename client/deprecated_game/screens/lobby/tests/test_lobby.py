from unittest import TestCase

import mock

from client.engine.features.user_input.events import UserTypedEvent
from client.engine.general_state.profile.profile import Profile
from client.engine.general_state.profile_manager import ProfileManager
from client.engine.visual_regression.visual_regression import VisualRegression
from client.game.screens.lobby.lobby import Lobby


class TestLobby(TestCase):
    @mock.patch("client.engine.general_state.profile_manager.Persistence")
    def _initialize_test_profile(self, m_persistence):
        profile = Profile(
            key="test_profile",
            id="player_id",
            game_id="game_id",
            game_event_pointer=None,
        )
        profile.set_name("Test Name")
        m_persistence.load.return_value = profile
        ProfileManager().set_profile("test_profile")

    def setUp(self):
        self._initialize_test_profile()
        self.lobby = Lobby()

    @mock.patch("client.game.commands.NewGame")
    def test_navigating_to_new_game(self, m_new_game_command):
        self.lobby.update(
            UserTypedEvent("1"),
        )
        m_new_game_command.assert_called_once()

    @mock.patch("client.game.commands.GoToJoinAGame")
    def test_navigating_to_join_a_game(self, m_go_to_join_a_game):
        self.lobby.update(
            UserTypedEvent("2"),
        )
        m_go_to_join_a_game.assert_called_once()

    @mock.patch("client.game.commands.GoToGameList")
    def test_navigating_to_game_list(self, m_go_to_game_list):
        self.lobby.update(
            UserTypedEvent("3"),
        )
        m_go_to_game_list.assert_called_once()

    @mock.patch("client.game.commands.GoToOptions")
    def test_navigating_to_options(self, m_go_to_options):
        self.lobby.update(
            UserTypedEvent("4"),
        )
        m_go_to_options.assert_called_once()

    @mock.patch("client.game.commands.GoToSetName")
    def test_navigating_to_set_name(self, m_go_to_set_name):
        self.lobby.update(
            UserTypedEvent("5"),
        )
        m_go_to_set_name.assert_called_once()

    @mock.patch("client.game.commands.GoToCredits")
    def test_navigating_to_credits(self, m_go_to_credits):
        self.lobby.update(
            UserTypedEvent("6"),
        )
        m_go_to_credits.assert_called_once()

    @mock.patch("client.engine.commands.PingTheServer")
    def test_pinging_the_server(self, m_ping):
        self.lobby.update(
            UserTypedEvent("p"),
        )
        m_ping.assert_called_once()

    @mock.patch("client.engine.commands.QuitGame")
    def test_quitting_the_game(self, m_quit):
        self.lobby.update(
            UserTypedEvent("escape"),
        )
        m_quit.assert_called_once()

    def test_visual_regression(self):
        VisualRegression.assert_matches_snapshot(
            self.lobby, "./client/game/screens/lobby/tests/screenshots/lobby.png"
        )
