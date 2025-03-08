import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.general_state.profile_what import ProfileWhat
from client.engine.primitives.event_handler import EventHandler
from client.engine.sound.music import Music
from client.engine.sound.sound import Sound

from .events import PlayMusicEvent, PlaySoundEvent, TurnSoundOffEvent, TurnSoundOnEvent

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class TurnSoundOnEventHandler(EventHandler[TurnSoundOnEvent]):
    def handle(self, event: "TurnSoundOnEvent") -> None:
        profile_what = ProfileWhat()
        profile_what.profile.set_sound_on()


class TurnSoundOffEventHandler(EventHandler[TurnSoundOffEvent]):
    def handle(self, event: "TurnSoundOffEvent") -> None:
        profile_what = ProfileWhat()
        profile_what.profile.set_sound_off()


class PlaySoundEventHandler(EventHandler[PlaySoundEvent]):
    def handle(self, event: "PlaySoundEvent") -> None:
        profile_what = ProfileWhat()
        # TODO: Event.sound is an id, not a path
        # but the sound module expects a path.
        if profile_what.profile.sound_on:
            Sound.play(event.sound)


class PlayMusicEventHandler(EventHandler[PlayMusicEvent]):
    def handle(self, event: "PlayMusicEvent") -> None:
        profile_what = ProfileWhat()
        # TODO: Event.music is an id, not a path
        # but the music module expects a path.
        if profile_what.profile.sound_on:
            Music.load(event.music)
            Music.play()


handlers_map: Dict[Type["Event"], Any] = {
    TurnSoundOnEvent: TurnSoundOnEventHandler,
    TurnSoundOffEvent: TurnSoundOffEventHandler,
    PlaySoundEvent: PlaySoundEventHandler,
    PlayMusicEvent: PlayMusicEventHandler,
}
