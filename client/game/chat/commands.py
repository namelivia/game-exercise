from typing import TYPE_CHECKING

from client.engine.features.chat.events import ChatMessageInGameEvent
from client.engine.primitives.command import Command

from .events import SendChatRequestEvent

if TYPE_CHECKING:
    from client.engine.general_state.profile.profile import Profile
    from client.engine.general_state.queue import Queue

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


class RequestSendChat(Command):
    def __init__(self, profile: "Profile", queue: "Queue", message: str):
        super().__init__(profile, queue, f"Request sending the chat message:{message}")
        # We need to attach the in_game event id to the network request
        in_game_event = ChatMessageInGameEvent(profile.id, message, "pending")
        self.events = [
            in_game_event,
            SendChatRequestEvent(in_game_event.id, message),
        ]
