from client.engine.primitives.event_handler import EventHandler
from common.messages import (
    SendChatMessage,
    GameEventsMessage,  # I would like this not to be here
    ErrorMessage,
)
from .events import SendChatRequestEvent, SendChatNetworkRequestEvent
from client.engine.commands import (
    UpdateGame,  # I would like not to have this one here
)
from client.engine.chat.commands import (
    ChatMessageInGameCommand,
)
from .commands import (
    SendChat,
)
from common.events import (
    ChatMessageEvent as ChatMessageInGameEvent,  # TODO: akward
)

from client.engine.network.channel import Channel

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""

# ===== SERVER INGAME EVENTS COMMUNICATIONS ===== THIS ARE THE IN-GAME EVENTS PLACED BY THE SERVER


class ChatMessageInGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        ChatMessageInGameCommand(
            client_state.profile, client_state.queue, event.player_id, event.message
        ).execute()


#################################################################


class SendChatRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        SendChat(
            client_state.profile,
            client_state.queue,
            client_state.profile.game_id,
            event.message,
        ).execute()


class SendChatNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        request_data = self._encode(
            client_state.profile.game_id, client_state.profile.id, event.message
        )

        response = Channel.send_command(request_data)
        if response is not None:
            # TODO: Ideally I would like to split the game events message into chats and
            # other
            if isinstance(response, GameEventsMessage):
                # TODO: Maybe I should split this too to be an UpdateChat?
                UpdateGame(
                    client_state.profile, client_state.queue, response.events
                ).execute()
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Server error")
            # TODO: The chat feature should not know about this
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, game_id, profile_id, message):
        return SendChatMessage(game_id, profile_id, message)


handlers_map = {
    SendChatRequestEvent: SendChatRequestEventHandler,
    SendChatNetworkRequestEvent: SendChatNetworkRequestEventHandler,
    ChatMessageInGameEvent: ChatMessageInGameEventHandler,
}
