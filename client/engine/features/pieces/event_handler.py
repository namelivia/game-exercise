import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.features.network.commands import SendNetworkRequest
from client.engine.general_state.profile_manager import ProfileManager
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
        PlayerPlacedSymbolInGameCommand(
            event.event_id,
            event.player_id,
            event.position,
        ).execute()


class PlaceASymbolRequestEventHandler(EventHandler[PlaceASymbolRequestEvent]):
    def handle(self, event: "PlaceASymbolRequestEvent") -> None:
        profile_manager = ProfileManager()
        game_id = profile_manager.profile.game_id
        if game_id is None:
            raise Exception("Trying to place symbol with no game")
        PlaceASymbol(
            game_id,
            event.event_id,
            event.position,
        ).execute()


class PlaceASymbolNetworkRequestEventHandler(
    EventHandler[PlaceASymbolNetworkRequestEvent]
):
    def on_success(self, event, response):
        if isinstance(response, SymbolPlacedConfirmation):
            SymbolPlacedConfirmedCommand(response.event_id).execute()
        if isinstance(response, ErrorMessage):
            logger.error(f"[ERROR][Server] {response.message}")
            SymbolPlacedErroredCommand(event.event_id).execute()

    def on_error(self, event):
        logger.error("[ERROR][Server] Server unreacheable")
        SymbolPlacedErroredCommand(event.event_id).execute()

    def handle(self, event: "PlaceASymbolNetworkRequestEvent") -> None:
        profile_manager = ProfileManager()
        game_id = profile_manager.profile.game_id
        if game_id is None:
            raise Exception("Trying to place symbol with no game")
        request_data = self._encode(
            game_id,
            event.event_id,
            profile_manager.profile.id,
            event.position,
        )

        SendNetworkRequest(request_data, self.on_success, self.on_error)

    def _encode(
        self, game_id: "UUID", event_id: "UUID", profile_id: "UUID", position: int
    ) -> PlaceASymbolMessage:
        return PlaceASymbolMessage(game_id, event_id, profile_id, position)


handlers_map: Dict[Type["Event"], Any] = {
    PlaceASymbolRequestEvent: PlaceASymbolRequestEventHandler,
    PlaceASymbolNetworkRequestEvent: PlaceASymbolNetworkRequestEventHandler,
    PlayerPlacedSymbolInGameEvent: PlayerPlacedSymbolInGameEventHandler,
}
