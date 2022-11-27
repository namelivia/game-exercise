from client.engine.primitives.screen import Screen
from .ui import (
    GameIdIndicator,
    GameNameIndicator,
    Player1NameIndicator,
    Player2NameIndicator,
    Background,
    IntroAnimation,
    Events,
    Board,
    StatusIndicator,
    WinnerIndicator,
)
from client.game.chat.ui import ChatInput, ChatMessages
from client.engine.events import UserTypedEvent
from client.game.commands import PlaySound
from client.engine.chat.events import ChatMessageInGameEvent
from client.engine.events import (
    GameCreatedInGameEvent,
    PlayerJoinedInGameEvent,
    PlayerWinsInGameEvent,
    PlayerPlacedSymbolInGameEvent,
)


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
            RequestPlaceASymbol,
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

    def on_game_created(self, event):
        print(
            "New Game created event, do something play some music, update the internal state or something"
        )
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
        # TODO: Could we play a UI animation here???
        self.ui_elements[1].play()

    def on_player_joined(self, event):
        print(
            "New Player Joined event, do something play some music, update the internal state or something"
        )
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
        self.data["players"].append(event.player_id)
        self.data["status"] = "It is player 1 turn"

    def on_player_wins(self, event):
        print(
            "A player won the game, do something play some music, update the internal state or something"
        )
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
        self.data["winner"] = event.player_id
        self.data["status"] = "The game is finished"

    def on_player_placed_symbol(self, event):
        if event.player_id == self.data["players"][0]:
            self.data["board"][event.position] = "blue"
            self.data["status"] = "It is player 2 turn"
        else:
            self.data["board"][event.position] = "red"
            self.data["status"] = "It is player 1 turn"
        PlaySound(
            self.client_state.profile, self.client_state.queue, "select"
        ).execute()

    def on_chat_message(self, event):
        self.data["chat_messages"].append(
            {
                "player_id": event.player_id,
                "message": event.message,
            }
        )
        print(self.data["chat_messages"])
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
