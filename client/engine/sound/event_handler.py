import logging
from client.engine.primitives.event_handler import EventHandler
from .events import (
    TurnSoundOnEvent,
    TurnSoundOffEvent,
)

logger = logging.getLogger(__name__)


class TurnSoundOnEventHandler(EventHandler):
    def handle(self, event, client_state):
        client_state.profile.set_sound_on()


class TurnSoundOffEventHandler(EventHandler):
    def handle(self, event, client_state):
        client_state.profile.set_sound_off()


handlers_map = {
    TurnSoundOnEvent: TurnSoundOnEventHandler,
    TurnSoundOffEvent: TurnSoundOffEventHandler,
}
