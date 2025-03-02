import logging
from typing import TYPE_CHECKING, Dict, Type

from client.engine.primitives.event_handler import EventHandler
from client.engine.sound.music import Music
from client.engine.sound.sound import Sound

from .events import PlayMusicEvent, PlaySoundEvent, TurnSoundOffEvent, TurnSoundOnEvent

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState
    from client.engine.primitives.event import E, Event

logger = logging.getLogger(__name__)


class TurnSoundOnEventHandler(EventHandler[TurnSoundOnEvent]):
    def handle(self, event: "TurnSoundOnEvent", client_state: "ClientState") -> None:
        client_state.profile.set_sound_on()


class TurnSoundOffEventHandler(EventHandler[TurnSoundOffEvent]):
    def handle(self, event: "TurnSoundOffEvent", client_state: "ClientState") -> None:
        client_state.profile.set_sound_off()


class PlaySoundEventHandler(EventHandler[PlaySoundEvent]):
    def handle(self, event: "PlaySoundEvent", client_state: "ClientState") -> None:
        if client_state.profile.sound_on:
            Sound.play(event.sound)


class PlayMusicEventHandler(EventHandler[PlayMusicEvent]):
    def handle(self, event: "PlayMusicEvent", client_state: "ClientState") -> None:
        if client_state.profile.sound_on:
            Music.load(event.music)
            Music.play()


handlers_map: Dict[Type["E"], Type[EventHandler["E"]]] = {
    TurnSoundOnEvent: TurnSoundOnEventHandler,
    TurnSoundOffEvent: TurnSoundOffEventHandler,
    PlaySoundEvent: PlaySoundEventHandler,
    PlayMusicEvent: PlayMusicEventHandler,
}
