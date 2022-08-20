from unittest import TestCase
from client.game.screens.lobby.lobby import Lobby
from client.engine.events import UserTypedEvent
from client.engine.visual_regression.visual_regression import VisualRegression
import mock


class TestLobby(TestCase):
    def setUp(self):
        self.client_state = mock.Mock()
        self.client_state.clock.get.return_value = 0  # Initial time is 0
        self.client_state.profile.name = "TestPlayer"
        self.lobby = Lobby(self.client_state)

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
