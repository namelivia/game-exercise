from typing import Optional
from client.engine.primitives.event import InGameEvent, Event


class ChatMessageConfirmedInGameEvent(InGameEvent):
    def __init__(self, chat_message_event_id: str):
        super().__init__()
        self.chat_message_event_id = chat_message_event_id


class ChatMessageInGameEvent(InGameEvent):
    def __init__(
        self,
        player_id: str,
        message: str,
        confirmation: str,
        original_event_id: Optional[str] = None,
    ):
        super().__init__()
        self.player_id = player_id
        self.message = message
        self.confirmation = confirmation
        self.original_event_id = original_event_id


class SendChatNetworkRequestEvent(Event):
    def __init__(self, game_id: str, event_id: str, message: str):
        super().__init__()
        self.game_id = game_id
        self.event_id = event_id
        self.message = message


class ChatMessageErroredEvent(InGameEvent):
    # This indicates that a chat message wasn't sucessfully processed
    # by the server and therefore it needs to be rolled back.
    def __init__(self, chat_message_event_id: str):
        super().__init__()
        self.chat_message_event_id = chat_message_event_id
