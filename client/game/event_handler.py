from abc import ABC
from common.messages import (
    GameMessage,
    ErrorMessage,
    CreateAGameMessage,
    PlaceASymbolMessage,
    JoinAGameMessage,
    GetGameStatus,
)
from .events import (
    QuitGameEvent,
    ScreenTransitionEvent,
    NewGameRequestEvent,
    PlaceASymbolRequestEvent,
    JoinExistingGameEvent,
    InitiateGameEvent,
    RefreshGameStatusEvent,
    UpdateGameEvent,
    PlaySoundEvent,
    PlayerJoinedEvent,
    PlayerPlacedSymbolEvent,
    ClearInternalGameInformationEvent,
    SetInternalGameInformationEvent,
    CreateAGameNetworkRequestEvent,
    JoinAGameNetworkRequestEvent,
    PlaceASymbolNetworkRequestEvent,
)
from .screens.intro.intro import Intro
from .screens.lobby.lobby import Lobby
from .screens.new_game.new_game import NewGame
from .screens.join_game.join_game import JoinGame
from .screens.in_game.in_game import InGame
from .commands import (
    CreateAGame,
    JoinAGame,
    PlaceASymbol,
    RefreshGameStatus,
    GameCreatedCommand,
    PlayerJoinedCommand,
    PlayerPlacedSymbolCommand,
    BackToLobby,
    UpdateGame,
    InitiateGame
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


class EventHandler(ABC):
    def handle(self, event, client_state, graphics):
        pass


class QuitGameEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        import pygame  # This is pygame dependent
        import sys
        pygame.quit()
        sys.exit()


class PlaySoundEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
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


class GameCreatedEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        GameCreatedCommand(
            client_state.profile,
            client_state.queue,
            event.player_id
        ).execute()


class PlayerJoinedGenericEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        PlayerJoinedCommand(
            client_state.profile,
            client_state.queue,
            event.player_id
        ).execute()


class PlayerPlacedSymbolGenericEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        PlayerPlacedSymbolCommand(
            client_state.profile,
            client_state.queue,
            event.player_id,
            event.position
        ).execute()


class ScreenTransitionEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        # Could I just push the instances to the queue?
        if event.dest_screen == "intro":
            client_state.set_current_screen(
                Intro(client_state, graphics)
            )
        if event.dest_screen == "lobby":
            client_state.set_current_screen(
                Lobby(client_state, graphics)
            )
        if event.dest_screen == "new_game_screen":
            client_state.set_current_screen(
                NewGame(client_state, graphics)
            )
        if event.dest_screen == "join_a_game":
            client_state.set_current_screen(
                JoinGame(client_state, graphics)
            )


class InitiateGameEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        # TODO: Why is it not an screen transition event??? Just because it contains more data?
        client_state.set_current_screen(
            InGame(
                client_state,
                graphics,
                event.turn,
                event.board,
                event.events,
                event.game_id,
                event.name,
                event.player_1_id,
                event.player_2_id,
            )
        )


class UpdateGameEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        # What we are going to do know is to check for unprocessed events
        # there may be new events that have not been processed by the client,
        # How do we know that? using tha game_event_pointer.
        events = event.events
        game_event_pointer = client_state.profile.game_event_pointer
        unprocessed_events = events[game_event_pointer + 1:]
        # and now for each of this I would like to push them
        # to the queue
        for event in unprocessed_events:
            pass
            # self._handle_server_event(event, client_state)
        # And finally I would update the game event pointer
        game_event_pointer = client_state.profile.set_game_event_pointer(len(events) - 1)


class NewGameRequestEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        CreateAGame(
            client_state.profile,
            client_state.queue,
            event.new_game_name
        ).execute()


class ClearInternalGameInformationEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        client_state.profile.set_game(None)
        client_state.profile.set_game_event_pointer(None)


class SetInternalGameInformationEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        client_state.profile.set_game(event.game_id)
        client_state.profile.set_game_event_pointer(0)


class PlaceASymbolRequestEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        PlaceASymbol(
            client_state.profile,
            client_state.queue,
            client_state.profile.game_id,
            event.position
        ).execute()


class PlaceASymbolNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
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
                )
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Server error")
            BackToLobby(client_state.profile, client_state.queue)

    def _encode(self, game_id, profile_id, position):
        return PlaceASymbolMessage(game_id, profile_id, position)


class CreateAGameNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        request_data = self._encode(
            client_state.profile.id,
            event.new_game_name
        )

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameMessage):
                InitiateGame(
                    response.id,
                    response.name,
                    response.turn,
                    response.board,
                    response.events,
                    response.player_1_id,
                    response.player_2_id,
                )
            if isinstance(response, ErrorMessage):
                print("Error creating the game")
                BackToLobby(client_state.profile, client_state.queue)
        else:
            print("Server error")
            BackToLobby(client_state.profile, client_state.queue)

    def _encode(self, profile_id, new_game_name):
        return CreateAGameMessage(new_game_name, profile_id)


class JoinAGameNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        request_data = self._encode(client_state.profile.id, event.game_id)

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameMessage):
                InitiateGame(
                    response.id,
                    response.name,
                    response.turn,
                    response.board,
                    response.events,
                    response.player_1_id,
                    response.player_2_id,
                )
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Error Joining Game")
            BackToLobby(client_state.profile, client_state.queue)

    def _encode(self, profile_id, game_id):
        return JoinAGameMessage(game_id, profile_id)


class RefreshGameStatusNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        request_data = self._encode(event.game_id, client_state.profile.id)

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameMessage):
                UpdateGame(
                    response.id,
                    response.name,
                    response.turn,
                    response.board,
                    response.events,
                    response.player_1_id,
                    response.player_2_id,
                )
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Server error")
            BackToLobby(client_state.profile, client_state.queue)

    def _encode(self, game_id, profile_id):
        return GetGameStatus(game_id, profile_id)


class JoinExistingGameEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        JoinAGame(
            client_state.profile,
            client_state.queue,
            event.game_id
        ).execute()


class RefreshGameStatusEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        RefreshGameStatus(
            client_state.profile,
            client_state.queue,
            event.game_id
        ).execute()


class PlayerJoinedEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        # Update the ingame data to set the player
        # Put an event on the queue to play an animation
        pass


class PlayerPlacedSymbolEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        # Update the ingame data to set the player piece
        # Put an event on the queue to play an animation
        pass


handlers_map = {
    QuitGameEvent: QuitGameEventHandler,
    ScreenTransitionEvent: ScreenTransitionEventHandler,
    NewGameRequestEvent: NewGameRequestEventHandler,
    PlaceASymbolRequestEvent: PlaceASymbolRequestEventHandler,
    JoinExistingGameEvent: JoinExistingGameEventHandler,
    InitiateGameEvent: InitiateGameEventHandler,
    RefreshGameStatusEvent: RefreshGameStatusEventHandler,
    UpdateGameEvent: UpdateGameEventHandler,
    PlaySoundEvent: PlaySoundEventHandler,
    PlayerJoinedEvent: PlayerJoinedEventHandler,
    PlayerPlacedSymbolEvent: PlayerPlacedSymbolEventHandler,
    GameCreated: GameCreatedEventHandler,
    ClearInternalGameInformationEvent: ClearInternalGameInformationEventHandler,
    SetInternalGameInformationEvent: SetInternalGameInformationEventHandler,
    CreateAGameNetworkRequestEvent: CreateAGameNetworkRequestEventHandler,
    JoinAGameNetworkRequestEvent: JoinAGameNetworkRequestEventHandler,
    PlaceASymbolNetworkRequestEvent: PlaceASymbolNetworkRequestEventHandler,
    PlayerJoinedGenericEvent: PlayerJoinedGenericEventHandler,
    PlayerPlacedSymbolGenericEvent: PlayerPlacedSymbolEventHandler,  # TODO: This should be the GENERIC!
}


class EventHandler():

    def handle(self, event, client_state, graphics):
        if event is None:
            return
        print(event)
        try:
            handlers_map[type(event)]().handle(event, client_state, graphics)
        except KeyError:
            pass  # Unhandled event
