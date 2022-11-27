from client.engine.primitives.command import Command
from .events import (
    ChatMessageInGameEvent,
)

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


# This one seems specific
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
