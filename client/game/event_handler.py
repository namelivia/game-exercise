from client.primitives.event_handler import EventHandler
from common.messages import (
    GameMessage,
    ErrorMessage,
    PlaceASymbolMessage,
)
from client.events import (
    InitiateGameEvent
)
from .events import (
    ScreenTransitionEvent,
    PlaceASymbolRequestEvent,
    PlaySoundEvent,
    ClearInternalGameInformationEvent,
    PlaceASymbolNetworkRequestEvent,
)
from .screens.intro.intro import Intro
from .screens.lobby.lobby import Lobby
from .screens.new_game.new_game import NewGame
from .screens.join_game.join_game import JoinGame
from .screens.in_game.in_game import InGame
from client.commands import (
    UpdateGame,
    GameCreatedCommand,
    PlayerJoinedCommand,
    PlayerPlacedSymbolCommand,
)
from .commands import (
    PlaceASymbol,
    BackToLobby,
)
from common.events import (
    GameCreated,
    PlayerJoined as PlayerJoinedGenericEvent,  # TODO: akward
    PlayerPlacedSymbol as PlayerPlacedSymbolGenericEvent  # TODO: akward
)
from .sounds import (
    BackSound,
    SelectSound,
    StartGameSound,
    TypeSound,
    EraseSound
)

from client.network.channel import Channel

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


class PlaySoundEventHandler(EventHandler):
    def handle(self, event, client_state):
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


# ===== SERVER INGAME EVENTS COMMUNICATIONS ===== THIS ARE THE IN-GAME EVENTS PLACED BY THE SERVER
class GameCreatedEventHandler(EventHandler):
    def handle(self, event, client_state):
        GameCreatedCommand(
            client_state.profile,
            client_state.queue,
            event.player_id
        ).execute()


class PlayerJoinedGenericEventHandler(EventHandler):
    def handle(self, event, client_state):
        PlayerJoinedCommand(
            client_state.profile,
            client_state.queue,
            event.player_id
        ).execute()


class PlayerPlacedSymbolGenericEventHandler(EventHandler):
    def handle(self, event, client_state):
        PlayerPlacedSymbolCommand(
            client_state.profile,
            client_state.queue,
            event.player_id,
            event.position
        ).execute()

#################################################################


class InitiateGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        # TODO: Why is it not an screen transition event??? Just because it contains more data?
        # PlaySoundEvent('start_game'), This should be a command
        client_state.set_current_screen(
            InGame(
                client_state,
                event.game_data.turn,
                event.game_data.board,
                event.game_data.events,
                event.game_data.game_id,
                event.game_data.name,
                event.game_data.player_1_id,
                event.game_data.player_2_id,
            )
        )


class ScreenTransitionEventHandler(EventHandler):
    def handle(self, event, client_state):
        # Could I just push the instances to the queue?
        if event.dest_screen == "intro":
            client_state.set_current_screen(
                Intro(client_state)
            )
        if event.dest_screen == "lobby":
            client_state.set_current_screen(
                Lobby(client_state)
            )
        if event.dest_screen == "new_game_screen":
            client_state.set_current_screen(
                NewGame(client_state)
            )
        if event.dest_screen == "join_a_game":
            client_state.set_current_screen(
                JoinGame(client_state)
            )


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
            event.position
        ).execute()


class PlaceASymbolNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        request_data = self._encode(
            client_state.profile.game_id,
            client_state.profile.id,
            event.position
        )

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameMessage):
                UpdateGame(
                    client_state.profile,
                    client_state.queue,
                    response.id,
                    response.name,
                    response.turn,
                    response.board,
                    response.events,
                    response.player_1_id,
                    response.player_2_id,
                ).execute()
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Server error")
            BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, game_id, profile_id, position):
        return PlaceASymbolMessage(game_id, profile_id, position)


handlers_map = {
    ScreenTransitionEvent: ScreenTransitionEventHandler,
    PlaceASymbolRequestEvent: PlaceASymbolRequestEventHandler,
    PlaySoundEvent: PlaySoundEventHandler,
    GameCreated: GameCreatedEventHandler,
    ClearInternalGameInformationEvent: ClearInternalGameInformationEventHandler,
    PlaceASymbolNetworkRequestEvent: PlaceASymbolNetworkRequestEventHandler,
    InitiateGameEvent: InitiateGameEventHandler,
    PlayerJoinedGenericEvent: PlayerJoinedGenericEventHandler,
    PlayerPlacedSymbolGenericEvent: PlayerPlacedSymbolGenericEventHandler,
}


class EventHandler():

    def handle(self, event, client_state):
        try:
            handlers_map[type(event)]().handle(event, client_state)
        except KeyError:
            pass  # Unhandled event
