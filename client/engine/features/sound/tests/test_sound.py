from unittest import TestCase

import mock

from client.engine.event_handler import EventHandler
from client.engine.features.sound.commands import (
    PlayMusic,
    PlaySound,
    TurnSoundOff,
    TurnSoundOn,
)
from client.engine.features.sound.events import (
    PlayMusicEvent,
    PlaySoundEvent,
    TurnSoundOffEvent,
    TurnSoundOnEvent,
)
from client.engine.general_state.queue import Queue


class TestSound(TestCase):
    def setUp(self):
        self.profile = mock.Mock()
        self.profile.game_id = "game_id"
        self.profile.id = "player_id"
        self.queue = Queue()
        self.event_handler = EventHandler()

    def test_turning_the_sound_on(self):
        # The command is invoked
        TurnSoundOn(self.profile, self.queue).execute()

        event = self.queue.pop()
        assert isinstance(event, TurnSoundOnEvent)

        client_state = mock.Mock()
        client_state.profile = self.profile

        self.event_handler.handle(event, client_state)

        # The client state option is updated
        self.profile.set_sound_on.assert_called_once_with()

    def test_turning_the_sound_off(self):
        # The command is invoked
        TurnSoundOff(self.profile, self.queue).execute()

        event = self.queue.pop()
        assert isinstance(event, TurnSoundOffEvent)

        client_state = mock.Mock()
        client_state.profile = self.profile

        self.event_handler.handle(event, client_state)

        # The client state optioff is updated
        self.profile.set_sound_off.assert_called_once_with()

    @mock.patch("client.engine.features.sound.event_handler.Music.play")
    @mock.patch("client.engine.features.sound.event_handler.Music.load")
    def test_playing_music(self, m_load, m_play):
        # The command is invoked
        PlayMusic(self.profile, self.queue, "main_theme").execute()

        event = self.queue.pop()
        assert isinstance(event, PlayMusicEvent)

        client_state = mock.Mock()
        client_state.profile = self.profile

        self.event_handler.handle(event, client_state)
        m_load.assert_called_once_with("main_theme")
        m_play.assert_called_once_with()

    @mock.patch("client.engine.features.sound.event_handler.Sound.play")
    def test_playing_sound(self, m_play):
        # The command is invoked
        PlaySound(self.profile, self.queue, "back").execute()

        event = self.queue.pop()
        assert isinstance(event, PlaySoundEvent)

        client_state = mock.Mock()
        client_state.profile = self.profile

        self.event_handler.handle(event, client_state)
        m_play.assert_called_once_with("back")
