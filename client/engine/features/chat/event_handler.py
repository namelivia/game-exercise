import logging
from client.engine.primitives.event_handler import EventHandler
from common.messages import (
    ErrorMessage,
    SendChatMessage,
    ChatMessageConfirmation,
)
from client.game.chat.events import SendChatRequestEvent
from .events import (
    SendChatNetworkRequestEvent,
)
from client.engine.features.chat.commands import (
    ChatMessageConfirmedCommand,
    ChatMessageInGameCommand,
)
from .commands import (
    SendChat,
)
from common.events import (
    ChatMessageEvent as ChatMessageInGameEvent,  # TODO: akward
)

from client.engine.network.channel import Channel

logger = logging.getLogger(__name__)

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


# ===== SERVER INGAME EVENTS COMMUNICATIONS ===== THIS ARE THE IN-GAME EVENTS PLACED BY THE SERVER
class ChatMessageConfirmationHandler(EventHandler):
    def handle(self, event, client_state):
        ChatMessageConfirmedCommand(
            client_state.profile, client_state.queue, event.event_id
        ).execute()


class ChatMessageInGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        # This is a chat message coming from the server
        ChatMessageInGameCommand(
            client_state.profile,
            client_state.queue,
            event.event_id,
            event.player_id,
            event.message,
        ).execute()


class SendChatRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        SendChat(
            client_state.profile,
            client_state.queue,
            client_state.profile.game_id,
            event.event_id,
            event.message,
        ).execute()


class SendChatNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        request_data = self._encode(
            client_state.profile.game_id,
            event.event_id,
            client_state.profile.id,
            event.message,
        )

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, ChatMessageConfirmation):
                ChatMessageConfirmedCommand(
                    client_state.profile, client_state.queue, response.event_id
                ).execute()
            if isinstance(response, ErrorMessage):
                # TODO: Deal with the error properly
                logger.error(response.__dict__)
        else:
            # TODO: Deal with the error properly
            logger.error("Server error")
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, game_id, event_id, profile_id, message):
        return SendChatMessage(game_id, event_id, profile_id, message)


handlers_map = {
    SendChatRequestEvent: SendChatRequestEventHandler,
    SendChatNetworkRequestEvent: SendChatNetworkRequestEventHandler,
    # TODO: Typing issue: These two are not of type Event
    ChatMessageConfirmation: ChatMessageConfirmationHandler,
    ChatMessageInGameEvent: ChatMessageInGameEventHandler,
}
