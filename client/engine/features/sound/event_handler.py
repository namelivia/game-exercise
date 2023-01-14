import logging
from typing import TYPE_CHECKING, Any
from client.engine.primitives.event_handler import EventHandler
from client.engine.sound.sound import Sound
from client.engine.sound.music import Music
from .events import (
    TurnSoundOnEvent,
    TurnSoundOffEvent,
    PlaySoundEvent,
    PlayMusicEvent,
)

if TYPE_CHECKING:
    from client.engine.primitives.event import Event


logger = logging.getLogger(__name__)


class TurnSoundOnEventHandler(EventHandler):
    def handle(self, event: Event, client_state: Any) -> None:
        client_state.profile.set_sound_on()


class TurnSoundOffEventHandler(EventHandler):
    def handle(self, event: Event, client_state: Any) -> None:
        client_state.profile.set_sound_off()


# TODO: The paths should not be here, should be passed in
class PlaySoundEventHandler(EventHandler):
    def handle(self, event: PlaySoundEvent, client_state: Any) -> None:
        if client_state.profile.sound_on:
            if event.sound == "back":
                Sound.play("client/game/sounds/back.mp3")
            if event.sound == "select":
                Sound.play("client/game/sounds/select.mp3")
            if event.sound == "start_game":
                Sound.play("client/game/sounds/start_game.mp3")
            if event.sound == "type":
                Sound.play("client/game/sounds/type.mp3")
            if event.sound == "erase":
                Sound.play("client/game/sounds/erase.mp3")
            if event.sound == "user_joined":
                Sound.play("client/game/sounds/user_connected.mp3")


# TODO: The paths should not be here, should be passed in
class PlayMusicEventHandler(EventHandler):
    def handle(self, event: PlayMusicEvent, client_state: Any) -> None:
        if client_state.profile.sound_on:
            if event.music == "main_theme":
                Music.load("client/game/music/main_theme.mp3")
                Music.play()


handlers_map = {
    TurnSoundOnEvent: TurnSoundOnEventHandler,
    TurnSoundOffEvent: TurnSoundOffEventHandler,
    PlaySoundEvent: PlaySoundEventHandler,
    PlayMusicEvent: PlayMusicEventHandler,
}
