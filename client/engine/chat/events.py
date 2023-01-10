from client.engine.primitives.event import InGameEvent, Event

"""
Events contain an operation and the data needed in order to perform
the operation. Will be put on a queue and when handler will execute
that operation.
"""


class ChatMessageErroredEvent(InGameEvent):
    # This indicates that a chat message wasn't sucessfully processed
    # by the server and therefore it needs to be rolled back.
    def __init__(self, chat_message_event_id):
        super().__init__()
        self.chat_message_event_id = chat_message_event_id


class ChatMessageConfirmedInGameEvent(InGameEvent):
    def __init__(self, chat_message_event_id):
        super().__init__()
        self.chat_message_event_id = chat_message_event_id


class ChatMessageInGameEvent(InGameEvent):
    def __init__(self, player_id, message, original_event_id=None):
        super().__init__()
        self.player_id = player_id
        self.message = message
        self.original_event_id = original_event_id


class SendChatNetworkRequestEvent(Event):
    def __init__(self, game_id, event_id, message):
        super().__init__()
        self.game_id = game_id
        self.event_id = event_id
        self.message = message
