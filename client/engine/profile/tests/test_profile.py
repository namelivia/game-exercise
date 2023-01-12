from unittest import TestCase
from client.engine.general_state.queue import Queue
from client.engine.event_handler import EventHandler
from client.engine.profile.commands import SetProfile, NewProfile, ProfileIsSet
from client.engine.profile.events import (
    SetProfileEvent,
    NewProfileEvent,
    ProfileSetInGameEvent,
)
from client.engine.general_state.profile.profile import Profile
import mock


class TestProfile(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.profile.game_id = "game_id"
        self.profile.id = "player_id"
        self.queue = Queue()
        self.event_handler = EventHandler()

    @mock.patch("client.engine.profile.event_handler.ProfileIsSet")
    def test_setting_a_profile(self, m_profile_is_set_command):
        # The command is invoked whith an existing profile key
        SetProfile(self.profile, self.queue, "profile_1").execute()

        set_profile_event = self.queue.pop()
        assert isinstance(set_profile_event, SetProfileEvent)
        assert set_profile_event.key == "profile_1"

        client_state = mock.Mock()
        client_state.profile = self.profile
        client_state.queue = self.queue
        client_state.set_profile = mock.Mock()

        self.event_handler.handle(set_profile_event, client_state)

        # The profile key is set in the client state
        client_state.set_profile.assert_called_once_with("profile_1")

        # The comand letting the game know that the profile is set is issued
        m_profile_is_set_command.assert_called_once_with(
            self.profile, self.queue, "profile_1"
        )

    @mock.patch("client.engine.profile.event_handler.SetProfile")
    def test_creating_a_profile(self, m_set_profile):
        # The command is invoked
        NewProfile(self.profile, self.queue).execute()

        new_profile_event = self.queue.pop()
        assert isinstance(new_profile_event, NewProfileEvent)

        client_state = mock.Mock()
        client_state.profile = self.profile
        client_state.queue = self.queue
        client_state.new_profile = mock.Mock()
        client_state.new_profile.return_value = Profile(
            key="new_profile_key",
            id="some_id",
            game_id=None,
            game_event_pointer=None,
            sound_on=True,
        )
        self.event_handler.handle(new_profile_event, client_state)

        # The profile creation is requested in the client state
        client_state.new_profile.assert_called_once()

        # The comand setting this new profile as the profile is invoked
        m_set_profile.assert_called_once_with(
            self.profile, self.queue, "new_profile_key"
        )

    def test_letting_the_game_know_that_a_profile_is_set(self):
        #  TODO: This command is probably redundant and can be replaced with just an event

        # The command is invoked
        ProfileIsSet(self.profile, self.queue, "profile_1").execute()

        event = self.queue.pop()
        assert isinstance(event, ProfileSetInGameEvent)
        assert event.key == "profile_1"
