import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.general_state.client_state import ClientState
from client.engine.general_state.profile_what import ProfileWhat
from client.engine.network.channel import Channel
from client.engine.primitives.event_handler import EventHandler
from client.game.pieces.events import PlaceASymbolRequestEvent
from common.events import (
    PlayerPlacedSymbol as PlayerPlacedSymbolInGameEvent,  # TODO: akward
)
from common.messages import ErrorMessage, PlaceASymbolMessage, SymbolPlacedConfirmation

from .commands import (
    PlaceASymbol,
    PlayerPlacedSymbolInGameCommand,
    SymbolPlacedConfirmedCommand,
    SymbolPlacedErroredCommand,
)
from .events import PlaceASymbolNetworkRequestEvent

if TYPE_CHECKING:
    from uuid import UUID

    from client.engine.primitives.event import Event


logger = logging.getLogger(__name__)


class PlayerPlacedSymbolInGameEventHandler(EventHandler[PlayerPlacedSymbolInGameEvent]):
    def handle(self, event: "PlayerPlacedSymbolInGameEvent") -> None:
        client_state = ClientState()
        PlayerPlacedSymbolInGameCommand(
            client_state.queue,
            event.event_id,
            event.player_id,
            event.position,
        ).execute()


class PlaceASymbolRequestEventHandler(EventHandler[PlaceASymbolRequestEvent]):
    def handle(self, event: "PlaceASymbolRequestEvent") -> None:
        client_state = ClientState()
        profile_what = ProfileWhat()
        game_id = profile_what.profile.game_id
        if game_id is None:
            raise Exception("Trying to place symbol with no game")
        PlaceASymbol(
            client_state.queue,
            game_id,
            event.event_id,
            event.position,
        ).execute()


class PlaceASymbolNetworkRequestEventHandler(
    EventHandler[PlaceASymbolNetworkRequestEvent]
):
    def handle(self, event: "PlaceASymbolNetworkRequestEvent") -> None:
        client_state = ClientState()
        profile_what = ProfileWhat()
        game_id = profile_what.profile.game_id
        if game_id is None:
            raise Exception("Trying to place symbol with no game")
        request_data = self._encode(
            game_id,
            event.event_id,
            profile_what.profile.id,
            event.position,
        )

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, SymbolPlacedConfirmation):
                SymbolPlacedConfirmedCommand(
                    client_state.queue, response.event_id
                ).execute()
            if isinstance(response, ErrorMessage):
                logger.error(f"[ERROR][Server] {response.message}")
                SymbolPlacedErroredCommand(client_state.queue, event.event_id).execute()
        else:
            logger.error("[ERROR][Server] Server unreacheable")
            SymbolPlacedErroredCommand(client_state.queue, event.event_id).execute()

    def _encode(
        self, game_id: "UUID", event_id: "UUID", profile_id: "UUID", position: int
    ) -> PlaceASymbolMessage:
        return PlaceASymbolMessage(game_id, event_id, profile_id, position)


handlers_map: Dict[Type["Event"], Any] = {
    PlaceASymbolRequestEvent: PlaceASymbolRequestEventHandler,
    PlaceASymbolNetworkRequestEvent: PlaceASymbolNetworkRequestEventHandler,
    PlayerPlacedSymbolInGameEvent: PlayerPlacedSymbolInGameEventHandler,
}
