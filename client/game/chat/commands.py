from client.engine.primitives.command import Command
from .events import SendChatRequestEvent, SendChatNetworkRequestEvent

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


# These put events on the queue requesting server interactions.
# ===== REQUESTS =====
class RequestSendChat(Command):
    def __init__(self, profile, queue, message):
        super().__init__(profile, queue, f"Request sending the chat message:{message}")
        self.events = [SendChatRequestEvent(message)]


class SendChat(Command):
    def __init__(self, profile, queue, game_id, message):
        super().__init__(
            profile, queue, f"Send chat message on game {game_id}: {message}"
        )
        self.events = [SendChatNetworkRequestEvent(game_id, message)]
