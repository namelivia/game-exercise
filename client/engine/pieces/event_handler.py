from client.engine.primitives.event_handler import EventHandler
from common.messages import (
    GameEventsMessage,
    ErrorMessage,
    PlaceASymbolMessage,
)
from client.engine.commands import UpdateGame
from client.game.pieces.events import PlaceASymbolRequestEvent
from .events import (
    PlaceASymbolNetworkRequestEvent,
    PlayerPlacedSymbolInGameEvent,
)
from .commands import PlayerPlacedSymbolInGameCommand, PlaceASymbol

from client.engine.network.channel import Channel

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


class PlayerPlacedSymbolInGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        PlayerPlacedSymbolInGameCommand(
            client_state.profile, client_state.queue, event.player_id, event.position
        ).execute()


class PlaceASymbolRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        PlaceASymbol(
            client_state.profile,
            client_state.queue,
            client_state.profile.game_id,
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
            if isinstance(response, GameEventsMessage):
                UpdateGame(
                    client_state.profile, client_state.queue, response.events
                ).execute()
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Server error")
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, game_id, event_id, profile_id, position):
        return PlaceASymbolMessage(game_id, event_id, profile_id, position)


handlers_map = {
    PlaceASymbolRequestEvent: PlaceASymbolRequestEventHandler,
    PlaceASymbolNetworkRequestEvent: PlaceASymbolNetworkRequestEventHandler,
    PlayerPlacedSymbolInGameEvent: PlayerPlacedSymbolInGameEventHandler,
}
