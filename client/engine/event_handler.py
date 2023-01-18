import logging
from client.engine.primitives.event_handler import EventHandler as BaseEventHandler
from .events import (
    QuitGameEvent,
    SetInternalGameInformationEvent,
    NewGameRequestEvent,
    JoinExistingGameEvent,
    CreateAGameNetworkRequestEvent,
    JoinAGameNetworkRequestEvent,
    PingNetworkRequestEvent,
    GetGameListNetworkRequestEvent,
    SetPlayerNameEvent,
)
from .commands import (
    CreateAGame,
    JoinAGame,
    InitiateGame,
    UpdateGameList,
    ErrorGettingGameList,
    ErrorCreatingGame,
    ErrorJoiningGame,
)

from common.messages import (
    GameInfoMessage,
    ErrorMessage,
    CreateAGameMessage,
    JoinAGameMessage,
    PingRequestMessage,
    PingResponseMessage,
    GameListRequestMessage,
    GameListResponseMessage,
)
from client.engine.network.channel import Channel
from client.engine.features.chat.event_handler import (
    handlers_map as chat_event_handlers,
)
from client.engine.features.pieces.event_handler import (
    handlers_map as pieces_event_handlers,
)
from client.engine.features.profile.event_handler import (
    handlers_map as profile_event_handlers,
)
from client.engine.features.sound.event_handler import (
    handlers_map as sound_event_handlers,
)
from client.engine.features.synchronization.event_handler import (
    handlers_map as synchronization_event_handlers,
)
from .game_data import GameData

logger = logging.getLogger(__name__)
"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


# ======= GENERIC =======
class QuitGameEventHandler(BaseEventHandler):
    def handle(self, event, client_state):
        import pygame  # This is pygame dependent
        import sys

        pygame.quit()
        sys.exit()


# ======= GAME STATE SYNC =======
class SetInternalGameInformationEventHandler(BaseEventHandler):
    def handle(self, event, client_state):
        client_state.profile.set_game(event.game_id)
        client_state.profile.set_game_event_pointer(0)


class SetPlayerNameEventHandler(BaseEventHandler):
    def handle(self, event, client_state):
        client_state.profile.set_name(event.name)


class NewGameRequestEventHandler(BaseEventHandler):
    def handle(self, event, client_state):
        CreateAGame(
            client_state.profile, client_state.queue, event.new_game_name
        ).execute()


class JoinExistingGameEventHandler(BaseEventHandler):
    def handle(self, event, client_state):
        JoinAGame(client_state.profile, client_state.queue, event.game_id).execute()


class CreateAGameNetworkRequestEventHandler(BaseEventHandler):
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
                logger.error("Error creating the game")
                # This is too game specific, why not using hooks?
                # BackToLobby(client_state.profile, client_state.queue).execute()
        else:
            ErrorCreatingGame(
                client_state.profile,
                client_state.queue,
            ).execute()
            logger.error("Server error")
            # This should be done at game level
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, profile_id, new_game_name):
        return CreateAGameMessage(new_game_name, profile_id)


class JoinAGameNetworkRequestEventHandler(BaseEventHandler):
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
                logger.error(response.__dict__)
        else:
            ErrorJoiningGame(
                client_state.profile,
                client_state.queue,
            ).execute()
            logger.error("Error Joining Game")
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, profile_id, game_id):
        return JoinAGameMessage(game_id, profile_id)


class PingNetworkRequestEventHandler(BaseEventHandler):
    def handle(self, event, client_state):
        request_data = self._encode()

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, PingResponseMessage):
                logger.info("Ping request OK")
            if isinstance(response, ErrorMessage):
                logger.error(response.__dict__)
        else:
            logger.error("Error pinging the server")

    def _encode(self):
        return PingRequestMessage()


class GetGameListNetworkRequestEventHandler(BaseEventHandler):
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
                logger.info(response.__dict__)
        else:
            ErrorGettingGameList(
                client_state.profile,
                client_state.queue,
            ).execute()
            logger.error("Error retrieving the game list from the server")

    def _encode(self):
        return GameListRequestMessage()


common_handlers = {
    QuitGameEvent: QuitGameEventHandler,
    CreateAGameNetworkRequestEvent: CreateAGameNetworkRequestEventHandler,
    JoinAGameNetworkRequestEvent: JoinAGameNetworkRequestEventHandler,
    PingNetworkRequestEvent: PingNetworkRequestEventHandler,
    GetGameListNetworkRequestEvent: GetGameListNetworkRequestEventHandler,
    SetInternalGameInformationEvent: SetInternalGameInformationEventHandler,
    NewGameRequestEvent: NewGameRequestEventHandler,
    JoinExistingGameEvent: JoinExistingGameEventHandler,
    SetPlayerNameEvent: SetPlayerNameEventHandler,
}

handlers_map = {
    **common_handlers,
    **chat_event_handlers,
    **pieces_event_handlers,
    **profile_event_handlers,
    **sound_event_handlers,
    **synchronization_event_handlers,
}


class EventHandler:
    def handle(self, event, client_state):
        handlers_map[type(event)]().handle(event, client_state)
