import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.commands import InitiateGame
from client.engine.features.network.commands import SendNetworkRequest
from client.engine.general_state.profile_manager import ProfileManager
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

    from client.engine.primitives.event import Event


logger = logging.getLogger(__name__)


class NewGameRequestEventHandler(EventHandler[NewGameRequestEvent]):
    def handle(self, event: "NewGameRequestEvent") -> None:
        CreateAGame(event.new_game_name).execute()


class JoinExistingGameEventHandler(EventHandler[JoinExistingGameEvent]):
    def handle(self, event: "JoinExistingGameEvent") -> None:
        JoinAGame(event.game_id).execute()


class CreateAGameNetworkRequestEventHandler(
    EventHandler[CreateAGameNetworkRequestEvent]
):
    def on_success(self, event, response):
        if isinstance(response, GameInfoMessage):
            InitiateGame(
                GameData(response.id, response.name, response.players),
            ).execute()
            # This is too game specific, why not using hooks?
        if isinstance(response, ErrorMessage):
            ErrorCreatingGame().execute()
            logger.error("Error creating the game")
            # This is too game specific, why not using hooks?
            # BackToLobby().execute()

    def on_error(self, event):
        ErrorCreatingGame().execute()
        logger.error("Server error")
        # This should be done at game level
        # BackToLobby().execute()

    def handle(self, event: "CreateAGameNetworkRequestEvent") -> None:
        profile_manager = ProfileManager()
        request_data = self._encode(profile_manager.profile.id, event.new_game_name)

        SendNetworkRequest(request_data, self.on_success, self.on_error)

    def _encode(self, profile_id: "UUID", new_game_name: str) -> "CreateAGameMessage":
        return CreateAGameMessage(new_game_name, profile_id)


class JoinAGameNetworkRequestEventHandler(EventHandler[JoinAGameNetworkRequestEvent]):
    def on_success(self, event, response):
        if isinstance(response, GameInfoMessage):
            InitiateGame(
                GameData(response.id, response.name, response.players),
            ).execute()
        if isinstance(response, ErrorMessage):
            ErrorJoiningGame().execute()
            logger.error(response.__dict__)

    def on_error(self, event):
        ErrorJoiningGame().execute()
        logger.error("Error Joining Game")
        # BackToLobby().execute()

    def handle(self, event: "JoinAGameNetworkRequestEvent") -> None:
        profile_manager = ProfileManager()
        request_data = self._encode(profile_manager.profile.id, event.game_id)

        SendNetworkRequest(request_data, self.on_success, self.on_error)

    def _encode(self, profile_id: "UUID", game_id: "UUID") -> JoinAGameMessage:
        return JoinAGameMessage(game_id, profile_id)


handlers_map: Dict[Type["Event"], Any] = {
    CreateAGameNetworkRequestEvent: CreateAGameNetworkRequestEventHandler,
    JoinAGameNetworkRequestEvent: JoinAGameNetworkRequestEventHandler,
    NewGameRequestEvent: NewGameRequestEventHandler,
    JoinExistingGameEvent: JoinExistingGameEventHandler,
}
