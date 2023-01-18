from client.engine.primitives.command import Command
from client.engine.features.chat.events import ChatMessageInGameEvent
from .events import SendChatRequestEvent

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


class RequestSendChat(Command):
    def __init__(self, profile, queue, message):
        super().__init__(profile, queue, f"Request sending the chat message:{message}")
        # We need to attach the in_game event id to the network request
        in_game_event = ChatMessageInGameEvent(profile.id, message, "pending")
        self.events = [
            in_game_event,
            SendChatRequestEvent(in_game_event.id, message),
        ]
