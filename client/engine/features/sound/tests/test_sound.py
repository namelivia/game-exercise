from unittest import TestCase
from client.engine.general_state.queue import Queue
from client.engine.event_handler import EventHandler
from client.engine.features.sound.commands import TurnSoundOn, TurnSoundOff
from client.engine.features.sound.events import TurnSoundOnEvent, TurnSoundOffEvent
import mock


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
