from client.engine.primitives.event import Event

"""
Events contain an operation and the data needed in order to perform
the operation. Will be put on a queue and when handler will execute
that operation.
"""


class SendChatRequestEvent(Event):
    def __init__(self, message):
        super().__init__()
        self.message = message


class SendChatNetworkRequestEvent(Event):
    def __init__(self, game_id, message):
        super().__init__()
        self.game_id = game_id
        self.message = message
