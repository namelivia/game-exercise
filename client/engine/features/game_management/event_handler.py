import logging
from typing import TYPE_CHECKING
from client.engine.primitives.event_handler import EventHandler
from client.engine.network.channel import Channel
from .commands import (
    CreateAGame,
    JoinAGame,
    ErrorCreatingGame,
    ErrorJoiningGame,
)
from client.engine.commands import InitiateGame
from .events import (
    NewGameRequestEvent,
    JoinExistingGameEvent,
    CreateAGameNetworkRequestEvent,
    JoinAGameNetworkRequestEvent,
)
from common.messages import (
    GameInfoMessage,
    ErrorMessage,
    CreateAGameMessage,
    JoinAGameMessage,
)
from client.engine.game_data import GameData

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState


logger = logging.getLogger(__name__)


class NewGameRequestEventHandler(EventHandler):
    def handle(self, event: "NewGameRequestEvent", client_state: "ClientState") -> None:
        CreateAGame(
            client_state.profile, client_state.queue, event.new_game_name
        ).execute()


class JoinExistingGameEventHandler(EventHandler):
    def handle(
        self, event: "JoinExistingGameEvent", client_state: "ClientState"
    ) -> None:
        JoinAGame(client_state.profile, client_state.queue, event.game_id).execute()


class CreateAGameNetworkRequestEventHandler(EventHandler):
    def handle(
        self, event: "CreateAGameNetworkRequestEvent", client_state: "ClientState"
    ) -> None:
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

    def _encode(self, profile_id: str, new_game_name: str) -> "CreateAGameMessage":
        return CreateAGameMessage(new_game_name, profile_id)


class JoinAGameNetworkRequestEventHandler(EventHandler):
    def handle(
        self, event: "JoinAGameNetworkRequestEvent", client_state: "ClientState"
    ) -> None:
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

    def _encode(self, profile_id: str, game_id: str) -> JoinAGameMessage:
        return JoinAGameMessage(game_id, profile_id)


handlers_map = {
    CreateAGameNetworkRequestEvent: CreateAGameNetworkRequestEventHandler,
    JoinAGameNetworkRequestEvent: JoinAGameNetworkRequestEventHandler,
    NewGameRequestEvent: NewGameRequestEventHandler,
    JoinExistingGameEvent: JoinExistingGameEventHandler,
}
