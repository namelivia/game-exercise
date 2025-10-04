import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.external.foundational_wrapper import FoundationalWrapper
from client.engine.primitives.event_handler import EventHandler

from .events import PlayMusicEvent, PlaySoundEvent, StopMusicEvent

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class PlaySoundEventHandler(EventHandler[PlaySoundEvent]):
    def handle(self, event: "PlaySoundEvent") -> None:
        # TODO: Event.sound is an id, not a path
        # but the sound module expects a path.
        FoundationalWrapper.play_sound(event.sound)


class PlayMusicEventHandler(EventHandler[PlayMusicEvent]):
    def handle(self, event: "PlayMusicEvent") -> None:
        # TODO: Event.music is an id, not a path
        # but the music module expects a path.
        FoundationalWrapper.load_music(event.music)
        FoundationalWrapper.play_music()


class StopMusicEventHandler(EventHandler[StopMusicEvent]):
    def handle(self, event: "StopMusicEvent") -> None:
        FoundationalWrapper.stop_music()


handlers_map: Dict[Type["Event"], Any] = {
    PlaySoundEvent: PlaySoundEventHandler,
    PlayMusicEvent: PlayMusicEventHandler,
    StopMusicEvent: StopMusicEventHandler,
}
