import logging
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
)
from common.events import (
    PlayerPlacedSymbol as PlayerPlacedSymbolInGameEvent,  # TODO: akward
)

from client.engine.network.channel import Channel

logger = logging.getLogger(__name__)


class PlayerPlacedSymbolConfirmationHandler(EventHandler):
    def handle(self, event, client_state):
        SymbolPlacedConfirmedCommand(
            client_state.profile, client_state.queue, event.event_id
        ).execute()


class PlayerPlacedSymbolInGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        PlayerPlacedSymbolInGameCommand(
            client_state.profile,
            client_state.queue,
            event.event_id,
            event.player_id,
            event.position,
        ).execute()


class PlaceASymbolRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        PlaceASymbol(
            client_state.profile,
            client_state.queue,
            client_state.profile.game_id,
            event.event_id,
            event.position,
        ).execute()


class PlaceASymbolNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
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
                # TODO: Deal with the error properly
                logger.error(response.__dict__)
        else:
            # TODO: Deal with the error properly
            logger.error("Server error")
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, game_id, event_id, profile_id, position):
        return PlaceASymbolMessage(game_id, event_id, profile_id, position)


handlers_map = {
    PlaceASymbolRequestEvent: PlaceASymbolRequestEventHandler,
    PlaceASymbolNetworkRequestEvent: PlaceASymbolNetworkRequestEventHandler,
    SymbolPlacedConfirmation: PlayerPlacedSymbolConfirmationHandler,
    PlayerPlacedSymbolInGameEvent: PlayerPlacedSymbolInGameEventHandler,
}
