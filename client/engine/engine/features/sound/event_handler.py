from typing import TYPE_CHECKING, Any, Dict, Type

from engine.primitives.event_handler import EventHandler

from .backend.pygame.sound import SoundBackend
from .events import (
    PlayMusicEvent,
    PlaySoundEvent,
    StopMusicEvent,
    TurnSoundOffEvent,
    TurnSoundOnEvent,
)
from .state import State

if TYPE_CHECKING:
    from engine.primitives.event import Event


class PlaySoundEventHandler(EventHandler[PlaySoundEvent]):
    def handle(self, event: "PlaySoundEvent") -> None:
        # TODO: Event.sound is an id, not a path
        # but the sound module expects a path.
        if State().is_sound_on():
            SoundBackend.play_sound(event.sound)


class PlayMusicEventHandler(EventHandler[PlayMusicEvent]):
    def handle(self, event: "PlayMusicEvent") -> None:
        # TODO: Event.music is an id, not a path
        # but the music module expects a path.
        if State().is_sound_on():
            SoundBackend.load_music(event.music)
            SoundBackend.play_music()


class StopMusicEventHandler(EventHandler[StopMusicEvent]):
    def handle(self, event: "StopMusicEvent") -> None:
        SoundBackend.stop_music()


class TurnSoundOnEventHandler(EventHandler[TurnSoundOnEvent]):
    def handle(self, event: "TurnSoundOnEvent") -> None:
        State().set_sound_on()


class TurnSoundOffEventHandler(EventHandler[TurnSoundOffEvent]):
    def handle(self, event: "TurnSoundOffEvent") -> None:
        State().set_sound_off()


handlers_map: Dict[Type["Event"], Any] = {
    PlaySoundEvent: PlaySoundEventHandler,
    PlayMusicEvent: PlayMusicEventHandler,
    StopMusicEvent: StopMusicEventHandler,
    TurnSoundOnEvent: TurnSoundOnEventHandler,
    TurnSoundOffEvent: TurnSoundOffEventHandler,
}
