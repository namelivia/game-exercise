import logging
from typing import TYPE_CHECKING
from client.engine.primitives.event_handler import EventHandler
from common.messages import (
    ErrorMessage,
    PlaceASymbolMessage,
    SymbolPlacedConfirmation,
)
from client.game.pieces.events import PlaceASymbolRequestEvent
from .events import (
    PlaceASymbolNetworkRequestEvent,
)
from .commands import (
    PlayerPlacedSymbolInGameCommand,
    PlaceASymbol,
    SymbolPlacedConfirmedCommand,
    SymbolPlacedErroredCommand,
)
from common.events import (
    PlayerPlacedSymbol as PlayerPlacedSymbolInGameEvent,  # TODO: akward
)

from client.engine.network.channel import Channel

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState


logger = logging.getLogger(__name__)


class PlayerPlacedSymbolConfirmationHandler(EventHandler):
    def handle(
        self,
        event: "SymbolPlacedConfirmation",
        client_state: "ClientState",
    ) -> None:
        SymbolPlacedConfirmedCommand(
            client_state.profile, client_state.queue, event.event_id
        ).execute()


class PlayerPlacedSymbolInGameEventHandler(EventHandler):
    def handle(
        self, event: "PlayerPlacedSymbolInGameEvent", client_state: "ClientState"
    ) -> None:
        PlayerPlacedSymbolInGameCommand(
            client_state.profile,
            client_state.queue,
            event.event_id,
            event.player_id,
            event.position,
        ).execute()


class PlaceASymbolRequestEventHandler(EventHandler):
    def handle(
        self, event: "PlaceASymbolRequestEvent", client_state: "ClientState"
    ) -> None:
        PlaceASymbol(
            client_state.profile,
            client_state.queue,
            client_state.profile.game_id,
            event.event_id,
            event.position,
        ).execute()


class PlaceASymbolNetworkRequestEventHandler(EventHandler):
    def handle(
        self, event: "PlaceASymbolNetworkRequestEvent", client_state: "ClientState"
    ) -> None:
        request_data = self._encode(
            client_state.profile.game_id,
            event.event_id,
            client_state.profile.id,
            event.position,
        )

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, SymbolPlacedConfirmation):
                SymbolPlacedConfirmedCommand(
                    client_state.profile, client_state.queue, response.event_id
                ).execute()
            if isinstance(response, ErrorMessage):
                logger.error(f"[ERROR][Server] {response.message}")
                SymbolPlacedErroredCommand(
                    client_state.profile, client_state.queue, event.event_id
                ).execute()
        else:
            logger.error("[ERROR][Server] Server unreacheable")
            SymbolPlacedErroredCommand(
                client_state.profile, client_state.queue, event.event_id
            ).execute()

    def _encode(
        self, game_id: str, event_id: str, profile_id: str, position: int
    ) -> PlaceASymbolMessage:
        return PlaceASymbolMessage(game_id, event_id, profile_id, position)


handlers_map = {
    PlaceASymbolRequestEvent: PlaceASymbolRequestEventHandler,
    PlaceASymbolNetworkRequestEvent: PlaceASymbolNetworkRequestEventHandler,
    SymbolPlacedConfirmation: PlayerPlacedSymbolConfirmationHandler,
    PlayerPlacedSymbolInGameEvent: PlayerPlacedSymbolInGameEventHandler,
}
