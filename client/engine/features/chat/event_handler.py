import logging
from typing import TYPE_CHECKING, Dict, Type
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
    SendChat,
    ChatMessageInGameCommand,
    ChatMessageErroredCommand,
)
from common.events import (
    ChatMessageEvent as ChatMessageInGameEvent,  # TODO: akward
)

from client.engine.network.channel import Channel

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState
    from uuid import UUID
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class ChatMessageInGameEventHandler(EventHandler):
    def handle(
        self, event: "ChatMessageInGameEvent", client_state: "ClientState"
    ) -> None:
        # This is a chat message coming from the server
        ChatMessageInGameCommand(
            client_state.profile,
            client_state.queue,
            event.event_id,
            event.player_id,
            event.message,
        ).execute()


class SendChatRequestEventHandler(EventHandler):
    def handle(
        self, event: "SendChatRequestEvent", client_state: "ClientState"
    ) -> None:
        game_id = client_state.profile.game_id
        if game_id is None:
            raise Exception("No game event pointer, the player is not in a game")
        SendChat(
            client_state.profile,
            client_state.queue,
            game_id,
            event.event_id,
            event.message,
        ).execute()


class SendChatNetworkRequestEventHandler(EventHandler):
    def handle(
        self, event: "SendChatNetworkRequestEvent", client_state: "ClientState"
    ) -> None:
        game_id = client_state.profile.game_id
        if game_id is None:
            raise Exception("No game event pointer, the player is not playing a game")
        request_data = self._encode(
            game_id,
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
                logger.error(f"[ERROR][Server] {response.message}")
                ChatMessageErroredCommand(
                    client_state.profile, client_state.queue, event.event_id
                ).execute()
        else:
            logger.error("[ERROR][Server] Server unreacheable")
            ChatMessageErroredCommand(
                client_state.profile, client_state.queue, event.event_id
            ).execute()

    def _encode(
        self, game_id: "UUID", event_id: "UUID", profile_id: "UUID", message: str
    ) -> "SendChatMessage":
        return SendChatMessage(game_id, event_id, profile_id, message)


handlers_map: Dict[Type["Event"], Type[EventHandler]] = {
    SendChatRequestEvent: SendChatRequestEventHandler,
    SendChatNetworkRequestEvent: SendChatNetworkRequestEventHandler,
    ChatMessageInGameEvent: ChatMessageInGameEventHandler,
}
