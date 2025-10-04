import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.features.chat.commands import (
    ChatMessageConfirmedCommand,
    ChatMessageErroredCommand,
    ChatMessageInGameCommand,
    SendChat,
)
from client.engine.features.network.commands import SendNetworkRequest
from client.engine.general_state.profile_manager import ProfileManager
from client.engine.primitives.event_handler import EventHandler
from client.game.chat.events import SendChatRequestEvent
from common.events import ChatMessageEvent as ChatMessageInGameEvent  # TODO: akward
from common.messages import ChatMessageConfirmation, ErrorMessage, SendChatMessage

from .events import SendChatNetworkRequestEvent

if TYPE_CHECKING:
    from uuid import UUID

    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class ChatMessageInGameEventHandler(EventHandler[ChatMessageInGameEvent]):
    def handle(self, event: "ChatMessageInGameEvent") -> None:
        # This is a chat message coming from the server
        ChatMessageInGameCommand(
            event.event_id,
            event.player_id,
            event.message,
        ).execute()


class SendChatRequestEventHandler(EventHandler[SendChatRequestEvent]):
    def handle(self, event: "SendChatRequestEvent") -> None:
        profile_manager = ProfileManager()
        game_id = profile_manager.profile.game_id
        if game_id is None:
            raise Exception("No game event pointer, the player is not in a game")
        SendChat(
            game_id,
            event.event_id,
            event.message,
        ).execute()


class SendChatNetworkRequestEventHandler(EventHandler[SendChatNetworkRequestEvent]):

    def on_success(self, event, response):
        if isinstance(response, ChatMessageConfirmation):
            ChatMessageConfirmedCommand(response.event_id).execute()
        if isinstance(response, ErrorMessage):
            logger.error(f"[ERROR][Server] {response.message}")
            ChatMessageErroredCommand(event.event_id).execute()

    def on_error(self, event):
        logger.error("[ERROR][Server] Server unreacheable")
        ChatMessageErroredCommand(event.event_id).execute()

    def handle(self, event: "SendChatNetworkRequestEvent") -> None:
        profile_manager = ProfileManager()
        game_id = profile_manager.profile.game_id
        if game_id is None:
            raise Exception("No game event pointer, the player is not playing a game")
        request_data = self._encode(
            game_id,
            event.event_id,
            profile_manager.profile.id,
            event.message,
        )

        SendNetworkRequest(request_data, self.on_success, self.on_error)

    def _encode(
        self, game_id: "UUID", event_id: "UUID", profile_id: "UUID", message: str
    ) -> "SendChatMessage":
        return SendChatMessage(game_id, event_id, profile_id, message)


handlers_map: Dict[Type["Event"], Any] = {
    SendChatRequestEvent: SendChatRequestEventHandler,
    SendChatNetworkRequestEvent: SendChatNetworkRequestEventHandler,
    ChatMessageInGameEvent: ChatMessageInGameEventHandler,
}
