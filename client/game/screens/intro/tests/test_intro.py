from unittest import TestCase
# from client.events import UserTypedEvent
# from client.game.screens.intro.intro import Intro
import mock


class TestIntroScreen(TestCase):
    @mock.patch("client.game.commands.ToLobby")
    def test_escape_to_lobby(self, m_to_lobby):
        pass
        # User types escape and goes to the lobby
        # screen = Intro(mock.Mock())
        # screen.update(UserTypedEvent("escape"))
        # m_to_lobby.assert_called_once()

    @mock.patch("client.game.commands.ToLobby")
    def test_enter_to_lobby(self, m_to_lobby):
        pass
        # User types enter and goes to the lobby
        # screen = Intro(mock.Mock())
        # screen.update(UserTypedEvent("escape"))
        # m_to_lobby.assert_called_once()
