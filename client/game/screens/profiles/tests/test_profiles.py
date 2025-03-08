from unittest import TestCase

import mock

from client.engine.features.profile.events import UpdateProfilesInGameEvent
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.visual_regression.visual_regression import VisualRegression
from client.game.screens.profiles.profiles import Profiles


class TestProfiles(TestCase):
    def setUp(self):
        self.profiles = Profiles()

    @mock.patch("client.game.screens.profiles.profiles.SetProfile")
    @mock.patch("client.engine.primitives.screen.ClientState")
    def test_profiles(self, m_client_state, m_set_profile):
        m_client_state().clock.get.return_value = 0  # Initial time is 0
        # Empty screen
        VisualRegression.assert_matches_snapshot(
            self.profiles,
            "./client/game/screens/profiles/tests/screenshots/profiles_empty.png",
        )

        # Profile list retrieved from disk
        self.profiles.update(
            UpdateProfilesInGameEvent(
                [
                    {"name": "some profile"},
                    {"name": "another profile"},
                    {"name": "yet another profile"},
                ]
            )
        )

        # Screen lists all profiles
        VisualRegression.assert_matches_snapshot(
            self.profiles,
            "./client/game/screens/profiles/tests/screenshots/profiles_show_profiles.png",
        )

        self.profiles.update(
            UserTypedEvent("2"),
        )
        m_set_profile.assert_called_once_with(mock.ANY, mock.ANY, "another profile")
