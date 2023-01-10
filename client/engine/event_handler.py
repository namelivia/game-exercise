from client.engine.primitives.event_handler import EventHandler
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
    PingNetworkRequestEvent,
    GetGameListNetworkRequestEvent,
    TurnSoundOnEvent,
    TurnSoundOffEvent,
    SetPlayerNameEvent,
    GetProfilesEvent,
    SetProfileEvent,
    NewProfileEvent,
)
from .commands import (
    ProcessServerEvents,
    RefreshGameStatus,
    UpdateGame,
    CreateAGame,
    JoinAGame,
    InitiateGame,
    UpdateGameList,
    ErrorGettingGameList,
    ErrorCreatingGame,
    ErrorJoiningGame,
    UpdateProfiles,
    ProfileIsSet,
    SetProfile,
)
from common.messages import (
    GameInfoMessage,
    GameEventsMessage,
    ErrorMessage,
    GetGameStatus,
    CreateAGameMessage,
    JoinAGameMessage,
    PingRequestMessage,
    PingResponseMessage,
    GameListRequestMessage,
    GameListResponseMessage,
)
from client.engine.network.channel import Channel
from client.engine.persistence.persistence import Persistence
from .chat.event_handler import handlers_map as chat_event_handlers
from .pieces.event_handler import handlers_map as pieces_event_handlers
from .game_data import GameData

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


# ======= GENERIC =======
class QuitGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        import pygame  # This is pygame dependent
        import sys

        pygame.quit()
        sys.exit()


class TurnSoundOnEventHandler(EventHandler):
    def handle(self, event, client_state):
        client_state.profile.set_sound_on()


class TurnSoundOffEventHandler(EventHandler):
    def handle(self, event, client_state):
        client_state.profile.set_sound_off()


# ======= GAME STATE SYNC =======
class UpdateGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        events = event.events
        game_event_pointer = client_state.profile.game_event_pointer
        client_state.profile.set_game_event_pointer(game_event_pointer + len(events))
        ProcessServerEvents(client_state.profile, client_state.queue, events).execute()


class SetInternalGameInformationEventHandler(EventHandler):
    def handle(self, event, client_state):
        client_state.profile.set_game(event.game_id)
        client_state.profile.set_game_event_pointer(0)


class SetPlayerNameEventHandler(EventHandler):
    def handle(self, event, client_state):
        client_state.profile.set_name(event.name)


class RefreshGameStatusEventHandler(EventHandler):
    def handle(self, event, client_state):
        RefreshGameStatus(
            client_state.profile, client_state.queue, event.game_id, event.pointer
        ).execute()


class NewGameRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        CreateAGame(
            client_state.profile, client_state.queue, event.new_game_name
        ).execute()


class JoinExistingGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        JoinAGame(client_state.profile, client_state.queue, event.game_id).execute()


class RefreshGameStatusNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        request_data = self._encode(
            event.game_id, event.pointer, client_state.profile.id
        )

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameEventsMessage):
                UpdateGame(
                    client_state.profile, client_state.queue, response.events
                ).execute()
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Server error")
            # This should be done at game level
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, game_id, pointer, profile_id):
        return GetGameStatus(game_id, pointer, profile_id)


class CreateAGameNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        request_data = self._encode(client_state.profile.id, event.new_game_name)

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameInfoMessage):
                InitiateGame(
                    client_state.profile,
                    client_state.queue,
                    GameData(response.id, response.name, response.players),
                ).execute()
                # This is too game specific, why not using hooks?
            if isinstance(response, ErrorMessage):
                ErrorCreatingGame(
                    client_state.profile,
                    client_state.queue,
                ).execute()
                print("Error creating the game")
                # This is too game specific, why not using hooks?
                # BackToLobby(client_state.profile, client_state.queue).execute()
        else:
            ErrorCreatingGame(
                client_state.profile,
                client_state.queue,
            ).execute()
            print("Server error")
            # This should be done at game level
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, profile_id, new_game_name):
        return CreateAGameMessage(new_game_name, profile_id)


class JoinAGameNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        request_data = self._encode(client_state.profile.id, event.game_id)

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameInfoMessage):
                InitiateGame(
                    client_state.profile,
                    client_state.queue,
                    GameData(response.id, response.name, response.players),
                ).execute()
            if isinstance(response, ErrorMessage):
                ErrorJoiningGame(
                    client_state.profile,
                    client_state.queue,
                ).execute()
                print(response.__dict__)
        else:
            ErrorJoiningGame(
                client_state.profile,
                client_state.queue,
            ).execute()
            print("Error Joining Game")
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, profile_id, game_id):
        return JoinAGameMessage(game_id, profile_id)


class PingNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        request_data = self._encode()

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, PingResponseMessage):
                print("Ping request OK")
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Error pinging the server")

    def _encode(self):
        return PingRequestMessage()


class GetProfilesEventHandler(EventHandler):
    def handle(self, event, client_state):
        # TODO retrieve profiles from disk
        profiles = self._build_profiles_index(Persistence.list())
        UpdateProfiles(client_state.profile, client_state.queue, profiles).execute()

    def _build_profiles_index(self, profiles):
        return [{"name": profile} for profile in profiles if profile != ".gitkeep"]


class SetProfileEventHandler(EventHandler):
    def handle(self, event, client_state):
        client_state.set_profile(event.key)
        ProfileIsSet(client_state.profile, client_state.queue, event.key).execute()


class NewProfileEventHandler(EventHandler):
    def handle(self, event, client_state):
        new_profile_key = client_state.new_profile().key
        SetProfile(client_state.profile, client_state.queue, new_profile_key).execute()


class GetGameListNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        request_data = self._encode()

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameListResponseMessage):
                UpdateGameList(
                    client_state.profile, client_state.queue, response.games
                ).execute()
            if isinstance(response, ErrorMessage):
                ErrorGettingGameList(
                    client_state.profile,
                    client_state.queue,
                ).execute()
                print(response.__dict__)
        else:
            ErrorGettingGameList(
                client_state.profile,
                client_state.queue,
            ).execute()
            print("Error retrieving the game list from the server")

    def _encode(self):
        return GameListRequestMessage()


common_handlers = {
    QuitGameEvent: QuitGameEventHandler,
    UpdateGameEvent: UpdateGameEventHandler,
    RefreshGameStatusEvent: RefreshGameStatusEventHandler,
    RefreshGameStatusNetworkRequestEvent: RefreshGameStatusNetworkRequestEventHandler,
    CreateAGameNetworkRequestEvent: CreateAGameNetworkRequestEventHandler,
    JoinAGameNetworkRequestEvent: JoinAGameNetworkRequestEventHandler,
    PingNetworkRequestEvent: PingNetworkRequestEventHandler,
    GetGameListNetworkRequestEvent: GetGameListNetworkRequestEventHandler,
    GetProfilesEvent: GetProfilesEventHandler,
    SetProfileEvent: SetProfileEventHandler,
    NewProfileEvent: NewProfileEventHandler,
    SetInternalGameInformationEvent: SetInternalGameInformationEventHandler,
    NewGameRequestEvent: NewGameRequestEventHandler,
    TurnSoundOnEvent: TurnSoundOnEventHandler,
    TurnSoundOffEvent: TurnSoundOffEventHandler,
    JoinExistingGameEvent: JoinExistingGameEventHandler,
    SetPlayerNameEvent: SetPlayerNameEventHandler,
}

handlers_map = {**common_handlers, **chat_event_handlers, **pieces_event_handlers}


class EventHandler:
    def handle(self, event, client_state):
        try:
            handlers_map[type(event)]().handle(event, client_state)
        except KeyError:
            pass  # Unhandled event
