from client.engine.primitives.command import Command
from client.engine.events import ChatMessageInGameEvent
from .events import (
    ScreenTransitionEvent,
    PlaceASymbolRequestEvent,
    SendChatRequestEvent,
    PlaceASymbolNetworkRequestEvent,
    SendChatNetworkRequestEvent,
    ClearInternalGameInformationEvent,
    PlaySoundEvent,
    PlayMusicEvent,
)

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


# These put events on the queue requesting server interactions.
# ===== REQUESTS =====
class RequestPlaceASymbol(Command):
    def __init__(self, profile, queue, position):
        super().__init__(
            profile, queue, f"Request placing a symbol on position {position}"
        )
        self.events = [PlaceASymbolRequestEvent(position)]


class RequestSendChat(Command):
    def __init__(self, profile, queue, message):
        super().__init__(profile, queue, f"Request sending the chat message:{message}")
        # We need to attach the in_game event id to the network request
        in_game_event = ChatMessageInGameEvent(profile.id, message)
        self.events = [
            SendChatRequestEvent(in_game_event.id, message),
            in_game_event,
        ]


# ===== SCREEN CHANGE REQUESTS =====
class BackToLobby(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move back to lobby")
        self.events = [
            ClearInternalGameInformationEvent(),
            PlaySoundEvent("back"),
            ScreenTransitionEvent("lobby"),
        ]


class ToLobby(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move forward to lobby")
        self.events = [
            PlaySoundEvent("select"),
            ScreenTransitionEvent("lobby"),
        ]


class PlaySound(Command):
    def __init__(self, profile, queue, sound_id):
        super().__init__(profile, queue, f"Playing sound {sound_id}")
        self.events = [
            PlaySoundEvent(sound_id),
        ]


class PlayMusic(Command):
    def __init__(self, profile, queue, music_id):
        super().__init__(profile, queue, f"Playing music {music_id}")
        self.events = [
            PlayMusicEvent(music_id),
        ]


class NewGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move to new game screen")
        self.events = [
            PlaySoundEvent("select"),
            ScreenTransitionEvent("new_game_screen"),
        ]


class GoToJoinAGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move to join game screen")
        self.events = [
            PlaySoundEvent("select"),
            ScreenTransitionEvent("join_a_game"),
        ]


class GoToGameList(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move to game list screen")
        self.events = [
            PlaySoundEvent("select"),
            ScreenTransitionEvent("game_list"),
        ]


class GoToOptions(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move to options screen")
        self.events = [
            PlaySoundEvent("select"),
            ScreenTransitionEvent("options"),
        ]


class GoToCredits(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move to options screen")
        self.events = [
            PlaySoundEvent("select"),
            ScreenTransitionEvent("credits"),
        ]


class GoToSetName(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move to set name screen")
        self.events = [
            PlaySoundEvent("select"),
            ScreenTransitionEvent("enter_name"),
        ]


class GoToProfiles(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move to the profiles screen")
        self.events = [
            PlaySoundEvent("select"),
            ScreenTransitionEvent("profiles"),
        ]


# ===== SERVER OUTBOUND COMMUNICATIONS =====
class PlaceASymbol(Command):
    def __init__(self, profile, queue, game_id, position):
        super().__init__(
            profile, queue, f"Place a symbol on game {game_id} on position {position}"
        )
        self.events = [PlaceASymbolNetworkRequestEvent(game_id, position)]


class SendChat(Command):
    def __init__(self, profile, queue, game_id, event_id, message):
        super().__init__(
            profile, queue, f"Send chat message on game {game_id}: {message}"
        )
        self.events = [SendChatNetworkRequestEvent(game_id, event_id, message)]
