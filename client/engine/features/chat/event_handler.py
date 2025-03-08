import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.features.chat.commands import (
    ChatMessageConfirmedCommand,
    ChatMessageErroredCommand,
    ChatMessageInGameCommand,
    SendChat,
)
from client.engine.general_state.profile_what import ProfileWhat
from client.engine.network.channel import Channel
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
        profile_what = ProfileWhat()
        game_id = profile_what.profile.game_id
        if game_id is None:
            raise Exception("No game event pointer, the player is not in a game")
        SendChat(
            game_id,
            event.event_id,
            event.message,
        ).execute()


class SendChatNetworkRequestEventHandler(EventHandler[SendChatNetworkRequestEvent]):
    def handle(self, event: "SendChatNetworkRequestEvent") -> None:
        profile_what = ProfileWhat()
        game_id = profile_what.profile.game_id
        if game_id is None:
            raise Exception("No game event pointer, the player is not playing a game")
        request_data = self._encode(
            game_id,
            event.event_id,
            profile_what.profile.id,
            event.message,
        )

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, ChatMessageConfirmation):
                ChatMessageConfirmedCommand(response.event_id).execute()
            if isinstance(response, ErrorMessage):
                logger.error(f"[ERROR][Server] {response.message}")
                ChatMessageErroredCommand(event.event_id).execute()
        else:
            logger.error("[ERROR][Server] Server unreacheable")
            ChatMessageErroredCommand(event.event_id).execute()

    def _encode(
        self, game_id: "UUID", event_id: "UUID", profile_id: "UUID", message: str
    ) -> "SendChatMessage":
        return SendChatMessage(game_id, event_id, profile_id, message)


handlers_map: Dict[Type["Event"], Any] = {
    SendChatRequestEvent: SendChatRequestEventHandler,
    SendChatNetworkRequestEvent: SendChatNetworkRequestEventHandler,
    ChatMessageInGameEvent: ChatMessageInGameEventHandler,
}
