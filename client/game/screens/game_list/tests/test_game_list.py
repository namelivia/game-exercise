from types import SimpleNamespace
from unittest import TestCase
from client.game.screens.game_list.game_list import GameList
from client.engine.visual_regression.visual_regression import VisualRegression
from client.engine.events import UpdateGameListEvent, UserTypedEvent
import mock


class TestGameList(TestCase):
    def setUp(self):
        self.client_state = mock.Mock()
        self.client_state.clock.get.return_value = 0  # Initial time is 0
        self.game_list = GameList(self.client_state)

    @mock.patch("client.engine.commands.RequestJoiningAGame")
    def test_game_list(self, m_request_joining_game):

        # Empty screen
        VisualRegression.assert_matches_snapshot(
            self.game_list,
            "./client/game/screens/game_list/tests/screenshots/game_list_empty.png"
        )

        # Game list received from server
        self.game_list.update(
            UpdateGameListEvent([
                SimpleNamespace(**{"id": "game_id_1", "name": "test game 1"}),
                SimpleNamespace(**{"id": "game_id_2", "name": "test game 2"}),
                SimpleNamespace(**{"id": "game_id_3", "name": "test game 3"}),
            ])
        )

        # Screen lists all games
        VisualRegression.assert_matches_snapshot(
            self.game_list,
            "./client/game/screens/game_list/tests/screenshots/game_list_show_games.png"
        )

        self.game_list.update(
            UserTypedEvent("2"),
        )
        m_request_joining_game.assert_called_once_with(mock.ANY, mock.ANY, "game_id_3")
