from client.engine.primitives.event import Event

"""
Events contain an operation and the data needed in order to perform
the operation. Will be put on a queue and when handler will execute
that operation.
"""


class ChatMessageInGameEvent(Event):
    def __init__(self, player_id, message):
        super().__init__()
        self.player_id = player_id
        self.message = message
