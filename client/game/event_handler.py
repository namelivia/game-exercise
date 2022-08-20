from client.engine.primitives.event_handler import EventHandler
from common.messages import (
    GameMessage,
    ErrorMessage,
    PlaceASymbolMessage,
    SendChatMessage,
)
from client.events import InitiateGameEvent
from .events import (
    ScreenTransitionEvent,
    PlaceASymbolRequestEvent,
    SendChatRequestEvent,
    PlaySoundEvent,
    PlayMusicEvent,
    ClearInternalGameInformationEvent,
    PlaceASymbolNetworkRequestEvent,
    SendChatNetworkRequestEvent,
)
from client.game.music import MainThemeMusic
from .screens.intro.intro import Intro
from .screens.lobby.lobby import Lobby
from .screens.new_game.new_game import NewGame
from .screens.join_game.join_game import JoinGame
from .screens.game_list.game_list import GameList
from .screens.options.options import Options
from .screens.in_game.in_game import InGame
from .screens.credits.credits import Credits
from .screens.enter_name.enter_name import EnterName
from client.commands import (
    UpdateGame,
    GameCreatedInGameCommand,
    PlayerJoinedInGameCommand,
    PlayerPlacedSymbolInGameCommand,
    ChatMessageInGameCommand,
)
from .commands import (
    PlaceASymbol,
    SendChat,
    BackToLobby,
    PlaySound,
)
from common.events import (
    GameCreated as GameCreatedInGameEvent,  # TODO: akward
    PlayerJoined as PlayerJoinedInGameEvent,  # TODO: akward
    PlayerPlacedSymbol as PlayerPlacedSymbolInGameEvent,  # TODO: akward
    ChatMessageEvent as ChatMessageInGameEvent,  # TODO: akward
)
from .sounds import (
    BackSound,
    SelectSound,
    StartGameSound,
    TypeSound,
    EraseSound,
    UserJoinedSound,
)

from client.network.channel import Channel

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


class PlaySoundEventHandler(EventHandler):
    def handle(self, event, client_state):
        if client_state.profile.sound_on:
            if event.sound == "back":
                BackSound().play()
            if event.sound == "select":
                SelectSound().play()
            if event.sound == "start_game":
                StartGameSound().play()
            if event.sound == "type":
                TypeSound().play()
            if event.sound == "erase":
                EraseSound().play()
            if event.sound == "user_joined":
                UserJoinedSound().play()


class PlayMusicEventHandler(EventHandler):
    def handle(self, event, client_state):
        if client_state.profile.sound_on:
            if event.music == "main_theme":
                MainThemeMusic().play()


# ===== SERVER INGAME EVENTS COMMUNICATIONS ===== THIS ARE THE IN-GAME EVENTS PLACED BY THE SERVER
class GameCreatedInGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        GameCreatedInGameCommand(
            client_state.profile, client_state.queue, event.player_id
        ).execute()


class PlayerJoinedInGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        PlayerJoinedInGameCommand(
            client_state.profile, client_state.queue, event.player_id
        ).execute()


class PlayerPlacedSymbolInGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        PlayerPlacedSymbolInGameCommand(
            client_state.profile, client_state.queue, event.player_id, event.position
        ).execute()


class ChatMessageInGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        ChatMessageInGameCommand(
            client_state.profile, client_state.queue, event.player_id, event.message
        ).execute()


#################################################################


class InitiateGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        # TODO: Why is it not an screen transition event??? Just because it contains more data?
        PlaySound(client_state.profile, client_state.queue, "start_game").execute()
        client_state.set_current_screen(
            InGame(
                client_state,
                event.game_data.events,
                event.game_data.id,
                event.game_data.name,
                event.game_data.players,
            )
        )


class ScreenTransitionEventHandler(EventHandler):
    def handle(self, event, client_state):
        # Could I just push the instances to the queue?
        if event.dest_screen == "intro":
            client_state.set_current_screen(Intro(client_state))
        if event.dest_screen == "lobby":
            client_state.set_current_screen(Lobby(client_state))
        if event.dest_screen == "new_game_screen":
            client_state.set_current_screen(NewGame(client_state))
        if event.dest_screen == "join_a_game":
            client_state.set_current_screen(JoinGame(client_state))
        if event.dest_screen == "game_list":
            client_state.set_current_screen(GameList(client_state))
        if event.dest_screen == "options":
            client_state.set_current_screen(Options(client_state))
        if event.dest_screen == "credits":
            client_state.set_current_screen(Credits(client_state))
        if event.dest_screen == "enter_name":
            client_state.set_current_screen(EnterName(client_state))


class ClearInternalGameInformationEventHandler(EventHandler):
    def handle(self, event, client_state):
        client_state.profile.set_game(None)
        client_state.profile.set_game_event_pointer(None)


class PlaceASymbolRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        PlaceASymbol(
            client_state.profile,
            client_state.queue,
            client_state.profile.game_id,
            event.position,
        ).execute()


class SendChatRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        SendChat(
            client_state.profile,
            client_state.queue,
            client_state.profile.game_id,
            event.message,
        ).execute()


class PlaceASymbolNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        request_data = self._encode(
            client_state.profile.game_id, client_state.profile.id, event.position
        )

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameMessage):
                UpdateGame(
                    client_state.profile, client_state.queue, response.events
                ).execute()
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Server error")
            BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, game_id, profile_id, position):
        return PlaceASymbolMessage(game_id, profile_id, position)


class SendChatNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        request_data = self._encode(
            client_state.profile.game_id, client_state.profile.id, event.message
        )

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameMessage):
                UpdateGame(
                    client_state.profile, client_state.queue, response.events
                ).execute()
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Server error")
            BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, game_id, profile_id, message):
        return SendChatMessage(game_id, profile_id, message)


handlers_map = {
    ScreenTransitionEvent: ScreenTransitionEventHandler,
    PlaceASymbolRequestEvent: PlaceASymbolRequestEventHandler,
    SendChatRequestEvent: SendChatRequestEventHandler,
    PlaySoundEvent: PlaySoundEventHandler,
    PlayMusicEvent: PlayMusicEventHandler,
    ClearInternalGameInformationEvent: ClearInternalGameInformationEventHandler,
    PlaceASymbolNetworkRequestEvent: PlaceASymbolNetworkRequestEventHandler,
    SendChatNetworkRequestEvent: SendChatNetworkRequestEventHandler,
    InitiateGameEvent: InitiateGameEventHandler,
    # In game events, these events define the status of the game
    GameCreatedInGameEvent: GameCreatedInGameEventHandler,
    PlayerJoinedInGameEvent: PlayerJoinedInGameEventHandler,
    PlayerPlacedSymbolInGameEvent: PlayerPlacedSymbolInGameEventHandler,
    ChatMessageInGameEvent: ChatMessageInGameEventHandler,
}


class EventHandler:
    def handle(self, event, client_state):
        try:
            handlers_map[type(event)]().handle(event, client_state)
        except KeyError:
            pass  # Unhandled event
