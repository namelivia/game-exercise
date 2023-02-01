from typing import TYPE_CHECKING
from client.engine.primitives.command import Command

if TYPE_CHECKING:
    from client.engine.general_state.profile.profile import Profile
    from client.engine.general_state.queue import Queue
    from uuid import UUID

from .events import (
    ChatMessageConfirmedInGameEvent,
    ChatMessageErroredEvent,
    ChatMessageInGameEvent,
    SendChatNetworkRequestEvent,
)


class ChatMessageConfirmedCommand(Command):
    # Let the game know that the chat message has been correctly delivered
    def __init__(self, profile: "Profile", queue: "Queue", event_id: "UUID"):
        super().__init__(profile, queue, f"Chat message event {event_id} confirmed")
        self.events = [ChatMessageConfirmedInGameEvent(event_id)]


class ChatMessageInGameCommand(Command):
    # Let the game know that there is a new chat message on the screen
    def __init__(
        self,
        profile: "Profile",
        queue: "Queue",
        event_id: "UUID",
        player_id: "UUID",
        message: str,
    ):
        super().__init__(profile, queue, f"Player {player_id} says: {message}")
        self.events = [
            ChatMessageInGameEvent(
                player_id, message, "OK", event_id  # This is the original event_id
            )
        ]


class SendChat(Command):
    # Send a chat message request to the server
    def __init__(
        self,
        profile: "Profile",
        queue: "Queue",
        game_id: "UUID",
        event_id: "UUID",
        message: str,
    ):
        super().__init__(
            profile, queue, f"Send chat message on game {game_id}: {message}"
        )
        self.events = [SendChatNetworkRequestEvent(game_id, event_id, message)]


class ChatMessageErroredCommand(Command):
    def __init__(self, profile: "Profile", queue: "Queue", event_id: "UUID"):
        super().__init__(profile, queue, f"Chat message event {event_id} errored")
        self.events = [ChatMessageErroredEvent(event_id)]
