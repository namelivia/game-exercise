import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.features.network.commands import SendNetworkRequest
from client.engine.general_state.profile_manager import ProfileManager
from client.engine.primitives.event_handler import E, EventHandler
from common.messages import ErrorMessage, GameEventsMessage, GetGameStatus

from .commands import ProcessServerEvents, RefreshGameStatus, UpdateGame
from .events import (
    RefreshGameStatusEvent,
    RefreshGameStatusNetworkRequestEvent,
    UpdateGameEvent,
)

if TYPE_CHECKING:
    from uuid import UUID

    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class UpdateGameEventHandler(EventHandler[UpdateGameEvent]):
    def handle(self, event: "UpdateGameEvent") -> None:
        profile_manager = ProfileManager()
        events = event.events
        game_event_pointer = profile_manager.profile.game_event_pointer
        if game_event_pointer is None:
            raise Exception("No game event pointer, the player is not playing a game")
        profile_manager.profile.set_game_event_pointer(game_event_pointer + len(events))
        ProcessServerEvents(events).execute()


class RefreshGameStatusEventHandler(EventHandler[RefreshGameStatusEvent]):
    def handle(self, event: "RefreshGameStatusEvent") -> None:
        RefreshGameStatus(event.game_id, event.pointer).execute()


class RefreshGameStatusNetworkRequestEventHandler(
    EventHandler[RefreshGameStatusNetworkRequestEvent]
):
    def on_success(self, event, response):
        if isinstance(response, GameEventsMessage):
            UpdateGame(response.events).execute()
        if isinstance(response, ErrorMessage):
            logger.error(response.__dict__)
            # TODO: Currently I'm not doing anything with this

    def on_error(self, event):
        logger.error("Server error")
        # TODO: Currently I'm not doing anything with this

    def handle(self, event: "RefreshGameStatusNetworkRequestEvent") -> None:
        profile_manager = ProfileManager()
        request_data = self._encode(
            event.game_id, event.pointer, profile_manager.profile.id
        )

        SendNetworkRequest(request_data, self.on_success, self.on_error)

    def _encode(
        self, game_id: "UUID", pointer: int, profile_id: "UUID"
    ) -> "GetGameStatus":
        return GetGameStatus(game_id, pointer, profile_id)


handlers_map: Dict[Type["Event"], Any] = {
    UpdateGameEvent: UpdateGameEventHandler,
    RefreshGameStatusEvent: RefreshGameStatusEventHandler,
    RefreshGameStatusNetworkRequestEvent: RefreshGameStatusNetworkRequestEventHandler,
}
