import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.commands import InitiateGame
from client.engine.network.channel import Channel
from client.engine.primitives.event_handler import EventHandler
from common.game_data import GameData
from common.messages import (
    CreateAGameMessage,
    ErrorMessage,
    GameInfoMessage,
    JoinAGameMessage,
)

from .commands import CreateAGame, ErrorCreatingGame, ErrorJoiningGame, JoinAGame
from .events import (
    CreateAGameNetworkRequestEvent,
    JoinAGameNetworkRequestEvent,
    JoinExistingGameEvent,
    NewGameRequestEvent,
)

if TYPE_CHECKING:
    from uuid import UUID

    from client.engine.general_state.client_state import ClientState
    from client.engine.primitives.event import Event


logger = logging.getLogger(__name__)


class NewGameRequestEventHandler(EventHandler[NewGameRequestEvent]):
    def handle(self, event: "NewGameRequestEvent", client_state: "ClientState") -> None:
        CreateAGame(
            client_state.profile, client_state.queue, event.new_game_name
        ).execute()


class JoinExistingGameEventHandler(EventHandler[JoinExistingGameEvent]):
    def handle(
        self, event: "JoinExistingGameEvent", client_state: "ClientState"
    ) -> None:
        JoinAGame(client_state.profile, client_state.queue, event.game_id).execute()


class CreateAGameNetworkRequestEventHandler(
    EventHandler[CreateAGameNetworkRequestEvent]
):
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

    def _encode(self, profile_id: "UUID", new_game_name: str) -> "CreateAGameMessage":
        return CreateAGameMessage(new_game_name, profile_id)


class JoinAGameNetworkRequestEventHandler(EventHandler[JoinAGameNetworkRequestEvent]):
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

    def _encode(self, profile_id: "UUID", game_id: "UUID") -> JoinAGameMessage:
        return JoinAGameMessage(game_id, profile_id)


handlers_map: Dict[Type["Event"], Any] = {
    CreateAGameNetworkRequestEvent: CreateAGameNetworkRequestEventHandler,
    JoinAGameNetworkRequestEvent: JoinAGameNetworkRequestEventHandler,
    NewGameRequestEvent: NewGameRequestEventHandler,
    JoinExistingGameEvent: JoinExistingGameEventHandler,
}
