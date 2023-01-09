from client.engine.primitives.event_handler import EventHandler
from common.messages import (
    ErrorMessage,
    SendChatMessage,
    ChatMessageConfirmation,
)
from .events import (
    SendChatRequestEvent,
    SendChatNetworkRequestEvent,
)
from client.engine.commands import (
    ChatMessageConfirmedCommand,
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
class ChatMessageConfirmationHandler(EventHandler):
    def handle(self, event, client_state):
        ChatMessageConfirmedCommand(
            client_state.profile, client_state.queue, event.event_id
        ).execute()


class ChatMessageInGameEventHandler(EventHandler):
    def handle(self, event, client_state):
        ChatMessageInGameCommand(
            client_state.profile, client_state.queue, event.player_id, event.message
        ).execute()


class SendChatRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        SendChat(
            client_state.profile,
            client_state.queue,
            client_state.profile.game_id,
            event.event_id,
            event.message,
        ).execute()


class SendChatNetworkRequestEventHandler(EventHandler):
    def handle(self, event, client_state):
        request_data = self._encode(
            client_state.profile.game_id,
            event.event_id,
            client_state.profile.id,
            event.message,
        )

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, ChatMessageConfirmation):
                ChatMessageConfirmedCommand(
                    client_state.profile, client_state.queue, response.event_id
                ).execute()
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Server error")
            # BackToLobby(client_state.profile, client_state.queue).execute()

    def _encode(self, game_id, event_id, profile_id, message):
        return SendChatMessage(game_id, event_id, profile_id, message)


handlers_map = {
    SendChatRequestEvent: SendChatRequestEventHandler,
    SendChatNetworkRequestEvent: SendChatNetworkRequestEventHandler,
    # In game events, these events define the status of the game
    ChatMessageConfirmation: ChatMessageConfirmationHandler,
    ChatMessageInGameEvent: ChatMessageInGameEventHandler,
}


class EventHandler:
    def handle(self, event, client_state):
        try:
            handlers_map[type(event)]().handle(event, client_state)
        except KeyError:
            pass  # Unhandled event
