from types import SimpleNamespace
from unittest import TestCase
from client.game.screens.profiles.profiles import Profiles
from client.engine.visual_regression.visual_regression import VisualRegression
from client.engine.events import UpdateProfilesEvent, UserTypedEvent
import mock


class TestProfiles(TestCase):
    def setUp(self):
        self.client_state = mock.Mock()
        self.client_state.clock.get.return_value = 0  # Initial time is 0
        self.profiles = Profiles(self.client_state)

    @mock.patch("client.engine.commands.RequestJoiningAGame")
    def test_profiles(self, m_request_joining_game):

        # Empty screen
        VisualRegression.assert_matches_snapshot(
            self.profiles,
            "./client/game/screens/profiles/tests/screenshots/profiles_empty.png",
        )

        # Game list received from server
        self.profiles.update(
            UpdateProfilesEvent(
                [
                    SimpleNamespace(**{"id": "game_id_1", "name": "test game 1"}),
                    SimpleNamespace(**{"id": "game_id_2", "name": "test game 2"}),
                    SimpleNamespace(**{"id": "game_id_3", "name": "test game 3"}),
                ]
            )
        )

        # Screen lists all games
        VisualRegression.assert_matches_snapshot(
            self.profiles,
            "./client/game/screens/profiles/tests/screenshots/profiles_show_games.png",
        )

        self.profiles.update(
            UserTypedEvent("2"),
        )
        m_request_joining_game.assert_called_once_with(mock.ANY, mock.ANY, "game_id_3")
