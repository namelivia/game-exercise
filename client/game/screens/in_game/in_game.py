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
from typing import TYPE_CHECKING, List, Any, Optional

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState

logger = logging.getLogger(__name__)


class InGame(Screen):
    def __init__(
        self,
        client_state: "ClientState",
        events: List[Any],
        game_id: str,
        name: str,
        players: List[str],
    ):
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
                {"fallback": None, "current": None},
                {"fallback": None, "current": None},
                {"fallback": None, "current": None},
                {"fallback": None, "current": None},
                {"fallback": None, "current": None},
                {"fallback": None, "current": None},
                {"fallback": None, "current": None},
                {"fallback": None, "current": None},
                {"fallback": None, "current": None},
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

    def _process_event(self, event: Any) -> None:
        self.events[event.__class__](event)

    # TODO: This_ is just for debugging
    def _advance_event_pointer(self) -> None:
        if self.data["event_pointer"] < len(self.data["events"]):
            self._process_event(self.data["events"][self.data["event_pointer"]])
            self.data["event_pointer"] += 1

    def on_user_typed(self, event: UserTypedEvent) -> None:
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
            if self._move_is_valid(int(event.key)):
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

    def _its_players_turn(self, player_id: str) -> bool:
        if player_id == self.data["players"][0]:
            return self.data["status"] == "It is player 1 turn"
        return self.data["status"] == "It is player 2 turn"

    def _position_is_valid(self, position: int) -> bool:
        return self.data["board"][position]["current"] is None

    def _move_is_valid(self, position: int) -> bool:
        return self._its_players_turn(
            self.client_state.profile.id
        ) and self._position_is_valid(position)

    def on_game_created(self, event: GameCreatedInGameEvent) -> None:
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
        # TODO: Could we play a UI animation here???
        self.ui_elements[1].play()

    def on_player_joined(self, event: PlayerJoinedInGameEvent) -> None:
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
        self.data["players"].append(event.player_id)
        self.data["status"] = "It is player 1 turn"

    def on_player_wins(self, event: PlayerWinsInGameEvent) -> None:
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
        self.data["winner"] = event.player_id
        self.data["status"] = "The game is finished"

    def _store_current_data_as_fallback(self, index: int) -> None:
        self.data["board"][index]["fallback"] = self.data["board"][index]["current"]

    def _get_color_for_player(self, player_id: str) -> str:
        if player_id == self.data["players"][0]:
            return "blue"
        return "red"

    def _get_new_status_after_placing(self, player_id: str) -> str:
        if player_id == self.data["players"][0]:
            return "It is player 2 turn"
        return "It is player 1 turn"

    def on_player_placed_symbol(self, event: PlayerPlacedSymbolInGameEvent) -> None:
        self._store_current_data_as_fallback(event.position)
        self.data["board"][event.position]["current"] = {
            "event_id": event.id,
            "color": self._get_color_for_player(event.player_id),
            "confirmation": event.confirmation,
        }
        self.data["status"] = self._get_new_status_after_placing(event.player_id)
        PlaySound(
            self.client_state.profile, self.client_state.queue, "select"
        ).execute()

    def on_chat_message(self, event: ChatMessageInGameEvent) -> None:
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

    def _get_chat_message_by_event_id(self, event_id: str) -> Optional[Any]:
        for entry in enumerate(self.data["chat_messages"]):
            if entry[1]["event_id"] == event_id:
                return entry
        return None  # This should not happen

    def on_chat_message_errored(self, event: ChatMessageErroredEvent) -> None:
        logger.info("[Screen] Chat message errored")
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
        index = self._get_chat_message_by_event_id(event.chat_message_event_id)[0]
        if self.data["chat_messages"][index]["confirmation"] == "pending":
            del self.data["chat_messages"][index]

    def on_chat_message_confirmed(self, event: ChatMessageConfirmedInGameEvent) -> None:
        logger.info("[Screen] Chat message confirmed")
        message = self._get_chat_message_by_event_id(event.chat_message_event_id)[1]
        message["confirmation"] = "OK"

    def _get_current_board_positions(self) -> List[int]:
        return [board_entry["current"] for board_entry in self.data["board"]]

    def _get_symbol_placement_by_event_id(self, event_id: str) -> Any:
        for board_entry in enumerate(self._get_current_board_positions()):
            if board_entry[1] is not None and board_entry[1]["event_id"] == event_id:
                return board_entry
        return None  # This should not happen

    def on_symbol_placement_confirmed(
        self, event: SymbolPlacedConfirmedInGameEvent
    ) -> None:
        logger.info("[Screen] Symbol placement confirmed")
        place = self._get_symbol_placement_by_event_id(event.place_symbol_event_id)[1]
        place["confirmation"] = "OK"

    def _fallback_to_previous_state(self, index: int) -> None:
        self.data["board"][index]["current"] = self.data["board"][index]["fallback"]

    def on_symbol_placement_errored(self, event: SymbolPlacedErroredEvent) -> None:
        logger.info("[Screen] Symbol placement errored")
        index = self._get_symbol_placement_by_event_id(event.place_symbol_event_id)[0]
        if self.data["board"][index]["current"]["confirmation"] == "pending":
            self._fallback_to_previous_state(index)
