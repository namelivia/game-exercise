from unittest import TestCase

import mock

from client.engine.event_handler import EventHandler
from client.engine.features.sound.commands import (
    PlayMusic,
    PlaySound,
    StopMusic,
    TurnSoundOff,
    TurnSoundOn,
)
from client.engine.features.sound.events import (
    PlayMusicEvent,
    PlaySoundEvent,
    StopMusicEvent,
    TurnSoundOffEvent,
    TurnSoundOnEvent,
)
from client.engine.general_state.options import Options
from client.engine.general_state.queue import Queue


class TestSound(TestCase):
    def setUp(self):
        self.event_handler = EventHandler()

        # Initialize an empty queue
        Queue().initialize(None)
        # And default options
        Options().initialize()

    def test_turning_the_sound_on(self):
        # The command is invoked
        TurnSoundOn().execute()

        event = Queue().pop()
        assert isinstance(event, TurnSoundOnEvent)

        self.event_handler.handle(event)

        # The options valus valuee is updated
        assert Options().sound_on is True

    def test_turning_the_sound_off(self):
        # The command is invoked
        TurnSoundOff().execute()

        event = Queue().pop()
        assert isinstance(event, TurnSoundOffEvent)

        self.event_handler.handle(event)

        # The options value is updated
        assert Options().sound_on is False

    @mock.patch(
        "client.engine.features.sound.event_handler.FoundationalWrapper.play_music"
    )
    @mock.patch(
        "client.engine.features.sound.event_handler.FoundationalWrapper.load_music"
    )
    def test_playing_music(self, m_load, m_play):
        # The command is invoked
        PlayMusic("main_theme").execute()

        event = Queue().pop()
        assert isinstance(event, PlayMusicEvent)

        # profile = self.profile

        self.event_handler.handle(event)
        m_load.assert_called_once_with("main_theme")
        m_play.assert_called_once_with()

    @mock.patch(
        "client.engine.features.sound.event_handler.FoundationalWrapper.stop_music"
    )
    def test_stopping_music(self, m_stop):
        # The command is invoked
        StopMusic().execute()

        event = Queue().pop()
        assert isinstance(event, StopMusicEvent)

        # profile = self.profile

        self.event_handler.handle(event)
        m_stop.assert_called_once_with()

    @mock.patch(
        "client.engine.features.sound.event_handler.FoundationalWrapper.play_sound"
    )
    def test_playing_sound(self, m_play):
        # The command is invoked
        PlaySound("back").execute()

        event = Queue().pop()
        assert isinstance(event, PlaySoundEvent)

        # profile = self.profile

        self.event_handler.handle(event)
        m_play.assert_called_once_with("back")
