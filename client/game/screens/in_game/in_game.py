import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from client.engine.events import (
    GameCreatedInGameEvent,
    PlayerJoinedInGameEvent,
    PlayerWinsInGameEvent,
)
from client.engine.features.chat.events import (
    ChatMessageConfirmedInGameEvent,
    ChatMessageErroredEvent,
    ChatMessageInGameEvent,
)
from client.engine.features.pieces.events import (
    PlayerPlacedSymbolInGameEvent,
    SymbolPlacedConfirmedInGameEvent,
    SymbolPlacedErroredEvent,
)
from client.engine.features.sound.commands import PlaySound
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.general_state.client_state import ClientState
from client.engine.general_state.profile_what import ProfileWhat
from client.engine.primitives.screen import Screen
from client.game.pieces.commands import RequestPlaceASymbol

from .ui import (
    Background,
    Board,
    ChatInput,
    ChatMessages,
    Events,
    GameIdIndicator,
    GameNameIndicator,
    IntroAnimation,
    Player1NameIndicator,
    Player2NameIndicator,
    StatusIndicator,
    WinnerIndicator,
)

if TYPE_CHECKING:
    from uuid import UUID


logger = logging.getLogger(__name__)


class InGame(Screen):
    def __init__(
        self,
        events: List[Any],
        game_id: "UUID",
        name: str,
        players: List["UUID"],
    ):
        super().__init__()

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
        from client.game.chat.commands import RequestSendChat
        from client.game.commands import BackToLobby

        # TODO: This_ is just for debugging
        if event.key == "return":
            if self.data["chat_focused"]:
                client_state = ClientState()
                RequestSendChat(
                    client_state.queue,
                    self.data["chat_input"],
                ).execute()
                self.data["chat_input"] = ""
                PlaySound(
                    client_state.queue,
                    "client/game/sounds/select.mp3",
                ).execute()
                return
            else:
                self._advance_event_pointer()
            return

        if event.key == "escape":
            if self.data["chat_focused"]:
                self.data["chat_focused"] = False
                chat_ui = self.ui_elements[7]
                if isinstance(chat_ui, ChatInput):
                    chat_ui.unfocus()
            else:
                client_state = ClientState()
                BackToLobby(client_state.queue).execute()
                return
        if event.key == "t":
            if not self.data["chat_focused"]:
                self.data["chat_focused"] = True
                chat_ui = self.ui_elements[7]
                if isinstance(chat_ui, ChatInput):
                    chat_ui.focus()
                return
        if event.key in "012345678":
            position = int(event.key)
            if self._move_is_valid(position):
                client_state = ClientState()
                RequestPlaceASymbol(client_state.queue, position).execute()
            return
        if event.key == "backspace" and self.data["chat_focused"]:
            client_state = ClientState()
            PlaySound(
                client_state.queue,
                "client/game/sounds/erase.mp3",
            ).execute()
            self.data["chat_input"] = self.data["chat_input"][:-1]
            return
        if self.data["chat_focused"]:
            client_state = ClientState()
            PlaySound(
                client_state.queue,
                "client/game/sounds/type.mp3",
            ).execute()
            self.data["chat_input"] += event.key

    def _its_players_turn(self, player_id: "UUID") -> bool:
        if player_id == self.data["players"][0]:
            return bool(self.data["status"] == "It is player 1 turn")
        return bool(self.data["status"] == "It is player 2 turn")

    def _position_is_valid(self, position: int) -> bool:
        return self.data["board"][position]["current"] is None

    def _move_is_valid(self, position: int) -> bool:
        profile_what = ProfileWhat()
        return self._its_players_turn(
            profile_what.profile.id
        ) and self._position_is_valid(position)

    def on_game_created(self, event: GameCreatedInGameEvent) -> None:
        client_state = ClientState()
        PlaySound(
            client_state.queue,
            "client/game/sounds/start_game.mp3",
        ).execute()
        # TODO: Could we play a UI animation here???
        animation = self.ui_elements[1]
        if isinstance(animation, IntroAnimation):
            animation.play()

    def on_player_joined(self, event: PlayerJoinedInGameEvent) -> None:
        client_state = ClientState()
        PlaySound(
            client_state.queue,
            "client/game/sounds/start_game.mp3",
        ).execute()
        self.data["players"].append(event.player_id)
        self.data["status"] = "It is player 1 turn"

    def on_player_wins(self, event: PlayerWinsInGameEvent) -> None:
        client_state = ClientState()
        PlaySound(
            client_state.queue,
            "client/game/sounds/start_game.mp3",
        ).execute()
        self.data["winner"] = event.player_id
        self.data["status"] = "The game is finished"

    def _store_current_data_as_fallback(self, index: int) -> None:
        self.data["board"][index]["fallback"] = self.data["board"][index]["current"]

    def _get_color_for_player(self, player_id: "UUID") -> str:
        if player_id == self.data["players"][0]:
            return "blue"
        return "red"

    def _get_new_status_after_placing(self, player_id: "UUID") -> str:
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
        client_state = ClientState()
        PlaySound(
            client_state.queue,
            "client/game/sounds/select.mp3",
        ).execute()

    def on_chat_message(self, event: ChatMessageInGameEvent) -> None:
        logger.info("[Screen] Incoming chat message")
        original_event_id = event.original_event_id
        if original_event_id is not None:
            # This is not working because the ingame event has another id
            # Check  if the message is already there waiting for confirmation
            already_there = self._get_chat_message_by_event_id(original_event_id)
            if not already_there:
                self.data["chat_messages"].append(
                    {
                        "event_id": event.id,
                        "player_id": event.player_id,
                        "message": event.message,
                        "confirmation": event.confirmation,
                    }
                )
                client_state = ClientState()
                PlaySound(
                    client_state.queue,
                    "client/game/sounds/start_game.mp3",
                ).execute()

    def _get_chat_message_by_event_id(self, event_id: "UUID") -> Optional[Any]:
        for entry in enumerate(self.data["chat_messages"]):
            if entry[1]["event_id"] == event_id:
                return entry
        return None  # This should not happen

    def on_chat_message_errored(self, event: ChatMessageErroredEvent) -> None:
        logger.info("[Screen] Chat message errored")
        client_state = ClientState()
        PlaySound(
            client_state.queue,
            "client/game/sounds/start_game.mp3",
        ).execute()
        message = self._get_chat_message_by_event_id(event.chat_message_event_id)
        if message is not None:
            index = message[0]
            if self.data["chat_messages"][index]["confirmation"] == "pending":
                del self.data["chat_messages"][index]

    def on_chat_message_confirmed(self, event: ChatMessageConfirmedInGameEvent) -> None:
        logger.info("[Screen] Chat message confirmed")
        message = self._get_chat_message_by_event_id(event.chat_message_event_id)
        if message is not None:
            message = message[1]
            message["confirmation"] = "OK"

    def _get_current_board_positions(self) -> List[Dict[str, Any]]:
        return [board_entry["current"] for board_entry in self.data["board"]]

    def _get_symbol_placement_by_event_id(self, event_id: "UUID") -> Any:
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
