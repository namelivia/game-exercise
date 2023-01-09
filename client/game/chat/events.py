from client.engine.primitives.event import Event

"""
Events contain an operation and the data needed in order to perform
the operation. Will be put on a queue and when handler will execute
that operation.
"""


class SendChatRequestEvent(Event):
    def __init__(self, event_id, message):
        super().__init__()
        self.event_id = event_id
        self.message = message


class SendChatNetworkRequestEvent(Event):
    def __init__(self, game_id, event_id, message):
        super().__init__()
        self.game_id = game_id
        self.event_id = event_id
        self.message = message
