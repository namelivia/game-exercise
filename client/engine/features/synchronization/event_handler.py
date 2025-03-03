import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.network.channel import Channel
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

    from client.engine.general_state.client_state import ClientState
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class UpdateGameEventHandler(EventHandler[UpdateGameEvent]):
    def handle(self, event: "UpdateGameEvent", client_state: "ClientState") -> None:
        events = event.events
        game_event_pointer = client_state.profile.game_event_pointer
        if game_event_pointer is None:
            raise Exception("No game event pointer, the player is not playing a game")
        client_state.profile.set_game_event_pointer(game_event_pointer + len(events))
        ProcessServerEvents(client_state.profile, client_state.queue, events).execute()


class RefreshGameStatusEventHandler(EventHandler[RefreshGameStatusEvent]):
    def handle(
        self, event: "RefreshGameStatusEvent", client_state: "ClientState"
    ) -> None:
        RefreshGameStatus(
            client_state.profile, client_state.queue, event.game_id, event.pointer
        ).execute()


class RefreshGameStatusNetworkRequestEventHandler(
    EventHandler[RefreshGameStatusNetworkRequestEvent]
):
    def handle(
        self, event: "RefreshGameStatusNetworkRequestEvent", client_state: "ClientState"
    ) -> None:
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
                logger.error(response.__dict__)
                # TODO: Currently I'm not doing anything with this
        else:
            logger.error("Server error")
            # TODO: Currently I'm not doing anything with this

    def _encode(
        self, game_id: "UUID", pointer: int, profile_id: "UUID"
    ) -> "GetGameStatus":
        return GetGameStatus(game_id, pointer, profile_id)


handlers_map: Dict[Type["Event"], Any] = {
    UpdateGameEvent: UpdateGameEventHandler,
    RefreshGameStatusEvent: RefreshGameStatusEventHandler,
    RefreshGameStatusNetworkRequestEvent: RefreshGameStatusNetworkRequestEventHandler,
}
