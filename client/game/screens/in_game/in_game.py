from client.engine.primitives.screen import Screen
from .ui import (
    GameIdIndicator,
    GameNameIndicator,
    Player1NameIndicator,
    Player2NameIndicator,
    Background,
    IntroAnimation,
    ChatInput,
    Events,
    ChatMessages,
    Board,
    StatusIndicator,
    WinnerIndicator,
)
import logging
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.features.sound.commands import PlaySound
from client.engine.events import (
    GameCreatedInGameEvent,
    PlayerJoinedInGameEvent,
    PlayerWinsInGameEvent,
)
from client.engine.features.chat.events import (
    ChatMessageInGameEvent,
    ChatMessageErroredEvent,
    ChatMessageConfirmedInGameEvent,
)
from client.engine.features.pieces.events import (
    PlayerPlacedSymbolInGameEvent,
    SymbolPlacedConfirmedInGameEvent,
    SymbolPlacedErroredEvent,
)
from client.game.pieces.commands import RequestPlaceASymbol

logger = logging.getLogger(__name__)


class InGame(Screen):
    def __init__(self, client_state, events, game_id, name, players):
        super().__init__(client_state)

        self.data = {
            "events": events,
            "game_id": game_id,
            "name": name,
            "winner": None,
            "players": players,
            "status": "waiting for player 2",
            "event_pointer": 0,
            "chat_input": "",
            "chat_focused": False,
            "chat_messages": [],
            "board": [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
        }

        self.ui_elements = [
            Background(),
            IntroAnimation(),
            GameIdIndicator(self.data["game_id"]),
            GameNameIndicator(self.data["name"]),
            Player1NameIndicator(self.data["players"][0]),
            Player2NameIndicator(),
            Events(self.data["events"], self.data["event_pointer"]),
            ChatInput(),
            ChatMessages(self.data["chat_messages"]),
            Board(),
            StatusIndicator(self.data["status"]),
            WinnerIndicator(self.data["winner"]),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            GameCreatedInGameEvent: self.on_game_created,
            PlayerJoinedInGameEvent: self.on_player_joined,
            PlayerWinsInGameEvent: self.on_player_wins,
            PlayerPlacedSymbolInGameEvent: self.on_player_placed_symbol,
            ChatMessageInGameEvent: self.on_chat_message,
            ChatMessageErroredEvent: self.on_chat_message_errored,
            ChatMessageConfirmedInGameEvent: self.on_chat_message_confirmed,
            SymbolPlacedConfirmedInGameEvent: self.on_symbol_placement_confirmed,
            SymbolPlacedErroredEvent: self.on_symbol_placement_errored,
        }

    def _process_event(self, event):
        self.events[event.__class__](event)

    # TODO: This_ is just for debugging
    def _advance_event_pointer(self):
        if self.data["event_pointer"] < len(self.data["events"]):
            self._process_event(self.data["events"][self.data["event_pointer"]])
            self.data["event_pointer"] += 1

    def on_user_typed(self, event):
        # Avoid circular import
        from client.game.commands import (
            BackToLobby,
        )
        from client.game.chat.commands import (
            RequestSendChat,
        )

        # TODO: This_ is just for debugging
        if event.key == "return":
            if self.data["chat_focused"]:
                RequestSendChat(
                    self.client_state.profile,
                    self.client_state.queue,
                    self.data["chat_input"],
                ).execute()
                self.data["chat_input"] = ""
                PlaySound(
                    self.client_state.profile, self.client_state.queue, "select"
                ).execute()
                return
            else:
                self._advance_event_pointer()
            return

        if event.key == "escape":
            if self.data["chat_focused"]:
                self.data["chat_focused"] = False
                self.ui_elements[7].unfocus()
            else:
                BackToLobby(
                    self.client_state.profile, self.client_state.queue
                ).execute()
                return
        if event.key == "t":
            if not self.data["chat_focused"]:
                self.data["chat_focused"] = True
                self.ui_elements[7].focus()
                return
        if event.key in "012345678":
            if self._position_is_valid(int(event.key)):
                RequestPlaceASymbol(
                    self.client_state.profile, self.client_state.queue, event.key
                ).execute()
            return
        if event.key == "backspace" and self.data["chat_focused"]:
            PlaySound(
                self.client_state.profile, self.client_state.queue, "erase"
            ).execute()
            self.data["chat_input"] = self.data["chat_input"][:-1]
            return
        if self.data["chat_focused"]:
            PlaySound(
                self.client_state.profile, self.client_state.queue, "type"
            ).execute()
            self.data["chat_input"] += event.key

    def _position_is_valid(self, position):
        # TODO: Write these validation rules, this is to validate in the client
        # to avoid always validating on the server side.
        # But it will be validated on the server anyway.
        return True

    def on_game_created(self, event):
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
        # TODO: Could we play a UI animation here???
        self.ui_elements[1].play()

    def on_player_joined(self, event):
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
        self.data["players"].append(event.player_id)
        self.data["status"] = "It is player 1 turn"

    def on_player_wins(self, event):
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
        self.data["winner"] = event.player_id
        self.data["status"] = "The game is finished"

    def on_player_placed_symbol(self, event):
        if event.player_id == self.data["players"][0]:
            self.data["board"][event.position] = {
                "event_id": event.id,
                "color": "blue",
                "confirmation": event.confirmation,
            }
            self.data["status"] = "It is player 2 turn"
        else:
            self.data["board"][event.position] = {
                "event_id": event.id,
                "color": "red",
                "confirmation": event.confirmation,
            }
            self.data["status"] = "It is player 1 turn"
        PlaySound(
            self.client_state.profile, self.client_state.queue, "select"
        ).execute()

    def on_chat_message(self, event):
        logger.info("[Screen] Incoming chat message")
        # This is not working because the ingame event has another id
        # Check  if the message is already there waiting for confirmation
        already_there = self._get_chat_message_by_event_id(event.original_event_id)
        if not already_there:
            self.data["chat_messages"].append(
                {
                    "event_id": event.id,
                    "player_id": event.player_id,
                    "message": event.message,
                    "confirmation": event.confirmation,
                }
            )
            PlaySound(
                self.client_state.profile, self.client_state.queue, "start_game"
            ).execute()

    def _get_chat_message_by_event_id(self, event_id):
        for entry in enumerate(self.data["chat_messages"]):
            if entry[1]["event_id"] == event_id:
                return entry
        return None  # This should not happen

    def on_chat_message_errored(self, event):
        logger.info("[Screen] Chat message errored")
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
        index = self._get_chat_message_by_event_id(event.chat_message_event_id)[0]
        if self.data["on_chat_messages"]["confirmation"] == "pending":
            del self.data["chat_messages"][index]

    def on_chat_message_confirmed(self, event):
        logger.info("[Screen] Chat message confirmed")
        message = self._get_chat_message_by_event_id(event.chat_message_event_id)[1]
        message["confirmation"] = "OK"

    def _get_symbol_placement_by_event_id(self, event_id):
        for board_entry in enumerate(self.data["board"]):
            if board_entry[1] is not None and board_entry[1]["event_id"] == event_id:
                return board_entry
        return None  # This should not happen

    def on_symbol_placement_confirmed(self, event):
        logger.info("[Screen] Symbol placement confirmed")
        place = self._get_symbol_placement_by_event_id(event.place_symbol_event_id)[1]
        place["confirmation"] = "OK"

    def on_symbol_placement_errored(self, event):
        logger.info("[Screen] Symbol placement errored")
        index = self._get_symbol_placement_by_event_id(event.place_symbol_event_id)[0]
        if self.data["board"]["confirmation"] == "pending":
            self.data["board"][index] = None
