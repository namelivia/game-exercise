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
        TurnSoundOn().execute()

        event = self.queue.pop()
        assert isinstance(event, TurnSoundOnEvent)

        # profile = self.profile

        self.event_handler.handle(event)

        # The client state option is updated
        self.profile.set_sound_on.assert_called_once_with()

    def test_turning_the_sound_off(self):
        # The command is invoked
        TurnSoundOff().execute()

        event = self.queue.pop()
        assert isinstance(event, TurnSoundOffEvent)

        # profile = self.profile

        self.event_handler.handle(event)

        # The client state optioff is updated
        self.profile.set_sound_off.assert_called_once_with()

    @mock.patch("client.engine.features.sound.event_handler.Music.play")
    @mock.patch("client.engine.features.sound.event_handler.Music.load")
    def test_playing_music(self, m_load, m_play):
        # The command is invoked
        PlayMusic("main_theme").execute()

        event = self.queue.pop()
        assert isinstance(event, PlayMusicEvent)

        # profile = self.profile

        self.event_handler.handle(event)
        m_load.assert_called_once_with("main_theme")
        m_play.assert_called_once_with()

    @mock.patch("client.engine.features.sound.event_handler.Sound.play")
    def test_playing_sound(self, m_play):
        # The command is invoked
        PlaySound("back").execute()

        event = self.queue.pop()
        assert isinstance(event, PlaySoundEvent)

        # profile = self.profile

        self.event_handler.handle(event)
        m_play.assert_called_once_with("back")
