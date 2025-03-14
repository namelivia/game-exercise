from unittest import TestCase

import mock

from client.engine.event_handler import EventHandler
from client.engine.features.profile.commands import (
    GetProfiles,
    NewProfile,
    ProfileIsSet,
    SetProfile,
    UpdateProfiles,
)
from client.engine.features.profile.events import (
    GetProfilesEvent,
    NewProfileEvent,
    ProfileSetInGameEvent,
    SetProfileEvent,
    UpdateProfilesInGameEvent,
)
from client.engine.general_state.profile.profile import Profile
from client.engine.general_state.queue import Queue


class TestProfile(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.profile.game_id = "game_id"
        self.profile.id = "player_id"
        self.queue = Queue()
        self.event_handler = EventHandler()

    @mock.patch("client.engine.features.profile.event_handler.ProfileIsSet")
    def test_setting_a_profile(self, m_profile_is_set_command):
        # The command is invoked whith an existing profile key
        SetProfile("profile_1").execute()

        set_profile_event = self.queue.pop()
        assert isinstance(set_profile_event, SetProfileEvent)
        assert set_profile_event.key == "profile_1"

        # profile = self.profile
        # queue = self.queue
        # set_profile = mock.Mock()

        self.event_handler.handle(set_profile_event)

        # The profile key is set in the client state
        # set_profile.assert_called_once_with("profile_1")

        # The comand letting the game know that the profile is set is issued
        m_profile_is_set_command.assert_called_once_with("profile_1")

    @mock.patch("client.engine.features.profile.event_handler.SetProfile")
    def test_creating_a_profile(self, m_set_profile):
        # The command is invoked
        NewProfile().execute()

        new_profile_event = self.queue.pop()
        assert isinstance(new_profile_event, NewProfileEvent)

        self.event_handler.handle(new_profile_event)

        # The profile creation is requested in the client state
        # new_profile.assert_called_once()

        # The comand setting this new profile as the profile is invoked
        # m_set_profile.assert_called_once_with("new_profile_key")

    def test_letting_the_game_know_that_a_profile_is_set(self):
        #  TODO: This command is probably redundant and can be replaced with just an event

        # The command is invoked
        ProfileIsSet("profile_1").execute()

        event = self.queue.pop()
        assert isinstance(event, ProfileSetInGameEvent)
        assert event.key == "profile_1"

    @mock.patch("client.engine.features.profile.event_handler.Persistence")
    @mock.patch("client.engine.features.profile.event_handler.UpdateProfiles")
    def test_getting_all_profiles(self, m_update_command, m_persistence):
        # Command is invoked
        GetProfiles().execute()

        event = self.queue.pop()
        assert isinstance(event, GetProfilesEvent)

        # profile = self.profile
        # queue = self.queue

        m_persistence.list = mock.Mock()
        # The persistence layer will retrieve the list of all profile namefiles
        m_persistence.list.return_value = [
            "profile_1",
            "profile_2",
            "profile_3",
            ".gitkeep",
        ]
        self.event_handler.handle(event)

        # The persistence layer has been queried
        m_persistence.list.assert_called_once_with()

        # The comand updating the profiles as the profile is invoked
        m_update_command.assert_called_once_with(
            [
                {"name": "profile_1"},
                {"name": "profile_2"},
                {"name": "profile_3"},
            ],
        )

    def test_updating_profiles(self):
        # Command is invoked
        UpdateProfiles(
            [
                {"name": "profile_1"},
                {"name": "profile_2"},
                {"name": "profile_3"},
            ],
        ).execute()

        event = self.queue.pop()

        # An event is raised for the screen to pickup
        assert isinstance(event, UpdateProfilesInGameEvent)
        assert event.profiles == [
            {"name": "profile_1"},
            {"name": "profile_2"},
            {"name": "profile_3"},
        ]
