import logging
from client.engine.primitives.event_handler import EventHandler
from client.engine.network.channel import Channel
from .events import (
    UpdateGameEvent,
    RefreshGameStatusEvent,
    RefreshGameStatusNetworkRequestEvent,
)
from .commands import (
    ProcessServerEvents,
    RefreshGameStatus,
    UpdateGame,
)
from common.messages import (
    GetGameStatus,
    GameEventsMessage,
    ErrorMessage,
)


logger = logging.getLogger(__name__)


class UpdateGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        events = event.events
        game_event_pointer = client_state.profile.game_event_pointer
        client_state.profile.set_game_event_pointer(game_event_pointer + len(events))
        ProcessServerEvents(client_state.profile, client_state.queue, events).execute()


class RefreshGameStatusEventHandler(EventHandler):
    def handle(self, event, client_state):
        RefreshGameStatus(
            client_state.profile, client_state.queue, event.game_id, event.pointer
        ).execute()


class RefreshGameStatusNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
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
        else:
            logger.error("Server error")
            # This should be done at game level
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, game_id, pointer, profile_id):
        return GetGameStatus(game_id, pointer, profile_id)


handlers_map = {
    UpdateGameEvent: UpdateGameEventHandler,
    RefreshGameStatusEvent: RefreshGameStatusEventHandler,
    RefreshGameStatusNetworkRequestEvent: RefreshGameStatusNetworkRequestEventHandler,
}
