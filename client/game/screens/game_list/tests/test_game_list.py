from types import SimpleNamespace
from unittest import TestCase

import mock

from client.engine.features.game_list.events import UpdateGameListEvent
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.general_state.queue import Queue
from client.engine.visual_regression.visual_regression import VisualRegression
from client.game.screens.game_list.game_list import GameList


class TestGameList(TestCase):

    def _initialize_test_queue(self):
        Queue().initialize(None)

    def setUp(self):
        self._initialize_test_queue()
        self.game_list = GameList()

    @mock.patch("client.game.screens.game_list.game_list.RequestJoiningAGame")
    def test_game_list(self, m_request_joining_game):
        # Empty screen
        VisualRegression.assert_matches_snapshot(
            self.game_list,
            "./client/game/screens/game_list/tests/screenshots/game_list_empty.png",
        )

        # Game list received from server
        self.game_list.update(
            UpdateGameListEvent(
                [
                    SimpleNamespace(**{"id": "game_id_1", "name": "test game 1"}),
                    SimpleNamespace(**{"id": "game_id_2", "name": "test game 2"}),
                    SimpleNamespace(**{"id": "game_id_3", "name": "test game 3"}),
                ]
            )
        )

        # Screen lists all games
        VisualRegression.assert_matches_snapshot(
            self.game_list,
            "./client/game/screens/game_list/tests/screenshots/game_list_show_games.png",
        )

        self.game_list.update(
            UserTypedEvent("2"),
        )
        m_request_joining_game.assert_called_once_with("game_id_3")
