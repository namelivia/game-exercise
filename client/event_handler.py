from client.primitives.event_handler import EventHandler
from .events import (
    QuitGameEvent,
    UpdateGameEvent,
    RefreshGameStatusEvent,
    SetInternalGameInformationEvent,
    RefreshGameStatusNetworkRequestEvent,
    NewGameRequestEvent,
    JoinExistingGameEvent,
    CreateAGameNetworkRequestEvent,
    JoinAGameNetworkRequestEvent,
)
from .commands import (
    ProcessServerEvents,
    RefreshGameStatus,
    UpdateGame,
    CreateAGame,
    JoinAGame,
    InitiateGame,
)
from common.messages import (
    GameMessage,
    ErrorMessage,
    GetGameStatus,
    CreateAGameMessage,
    JoinAGameMessage,
)
from client.network.channel import Channel
from client.game.game_data import CustomGameData  # TODO: I don't like this

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


# ======= GENERIC =======
class QuitGameEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        import pygame  # This is pygame dependent
        import sys
        pygame.quit()
        sys.exit()


# ======= GAME STATE SYNC =======
class UpdateGameEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        # What we are going to do know is to check for unprocessed events
        # there may be new events that have not been processed by the client,
        # How do we know that? using tha game_event_pointer.
        events = event.events
        game_event_pointer = client_state.profile.game_event_pointer
        unprocessed_events = events[game_event_pointer + 1:]
        game_event_pointer = client_state.profile.set_game_event_pointer(len(events) - 1)
        ProcessServerEvents(client_state.profile, client_state.queue, unprocessed_events).execute()


class SetInternalGameInformationEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        client_state.profile.set_game(event.game_id)
        client_state.profile.set_game_event_pointer(0)


class RefreshGameStatusEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        RefreshGameStatus(
            client_state.profile,
            client_state.queue,
            event.game_id
        ).execute()


class NewGameRequestEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        CreateAGame(
            client_state.profile,
            client_state.queue,
            event.new_game_name
        ).execute()


class JoinExistingGameEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        JoinAGame(
            client_state.profile,
            client_state.queue,
            event.game_id
        ).execute()


class RefreshGameStatusNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        request_data = self._encode(event.game_id, client_state.profile.id)

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameMessage):
                UpdateGame(
                    client_state.profile,
                    client_state.queue,
                    response.events
                ).execute()
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Server error")
            # This should be done at game level
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, game_id, profile_id):
        return GetGameStatus(game_id, profile_id)


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
                    client_state.profile,
                    client_state.queue,
                    # This is very game specific because it has CustomGameData
                    CustomGameData(
                        response.id,
                        response.name,
                        response.turn,
                        response.board,
                        response.player_1_id,
                        response.player_2_id,
                    )
                ).execute()
                # This is too game specific, why not using hooks?
            if isinstance(response, ErrorMessage):
                print("Error creating the game")
                # This is too game specific, why not using hooks?
                # BackToLobby(client_state.profile, client_state.queue).execute()
        else:
            print("Server error")
            # This should be done at game level
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, profile_id, new_game_name):
        return CreateAGameMessage(new_game_name, profile_id)


class JoinAGameNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        request_data = self._encode(client_state.profile.id, event.game_id)

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameMessage):
                InitiateGame(
                    client_state.profile,
                    client_state.queue,
                    # This is very game specific because it has CustomGameData
                    CustomGameData(
                        response.id,
                        response.name,
                        response.turn,
                        response.board,
                        response.player_1_id,
                        response.player_2_id,
                    )
                ).execute()
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Error Joining Game")
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, profile_id, game_id):
        return JoinAGameMessage(game_id, profile_id)


handlers_map = {
    QuitGameEvent: QuitGameEventHandler,
    UpdateGameEvent: UpdateGameEventHandler,
    RefreshGameStatusEvent: RefreshGameStatusEventHandler,
    RefreshGameStatusNetworkRequestEvent: RefreshGameStatusNetworkRequestEventHandler,
    CreateAGameNetworkRequestEvent: CreateAGameNetworkRequestEventHandler,
    JoinAGameNetworkRequestEvent: JoinAGameNetworkRequestEventHandler,
    SetInternalGameInformationEvent: SetInternalGameInformationEventHandler,
    NewGameRequestEvent: NewGameRequestEventHandler,
    JoinExistingGameEvent: JoinExistingGameEventHandler,
}


class EventHandler():

    def handle(self, event, client_state, graphics):
        try:
            handlers_map[type(event)]().handle(event, client_state, graphics)
        except KeyError:
            pass  # Unhandled event
