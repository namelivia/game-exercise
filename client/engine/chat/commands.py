from client.engine.primitives.command import Command
from .events import (
    ChatMessageConfirmedInGameEvent,
    ChatMessageErroredEvent,
    ChatMessageInGameEvent,
    SendChatNetworkRequestEvent,
)

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


class ChatMessageConfirmedCommand(Command):
    def __init__(self, profile, queue, event_id):
        super().__init__(profile, queue, f"Chat message event {event_id} confirmed")
        self.events = [ChatMessageConfirmedInGameEvent(event_id)]


class ChatMessageInGameCommand(Command):
    def __init__(self, profile, queue, player_id, message):
        super().__init__(profile, queue, f"Player {player_id} says: {message}")
        self.events = [
            ChatMessageInGameEvent(
                player_id, message
            )  # Event to be picked up by the screen event handler
            # I should pick this event on the game but
            # Still don't do anything with this event
        ]


class ChatMessageErroredCommand(Command):
    def __init__(self, profile, queue, player_id, event_id):
        super().__init__(profile, queue, f"Chat message event {event_id} errored")
        self.events = [
            ChatMessageErroredEvent(
                event_id
            )  # Event to be picked up by the screen event handler
            # I should pick this event on the game but
        ]


class SendChat(Command):
    # Send a chat message request to the server
    def __init__(self, profile, queue, game_id, event_id, message):
        super().__init__(
            profile, queue, f"Send chat message on game {game_id}: {message}"
        )
        self.events = [SendChatNetworkRequestEvent(game_id, event_id, message)]
