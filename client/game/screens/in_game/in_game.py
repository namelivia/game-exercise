from client.primitives.screen import Screen
from .ui import (
    GameIdIndicator,
    GameNameIndicator,
    Player1NameIndicator,
    Player2NameIndicator,
    EventPointerIndicator,
    Background,
    IntroAnimation,
    Events,
)
from client.events import UserTypedEvent
from client.game.commands import PlaySound
from client.events import (
    GameCreatedInGameEvent,
    PlayerJoinedInGameEvent,
    PlayerPlacedSymbolInGameEvent,
)


class InGame(Screen):
    def __init__(self, client_state, events, game_id, name, players):
        super().__init__(client_state)

        self.data = {
            "events": events,
            "game_id": game_id,
            "name": name,
            "players": players,
            "event_pointer": 0,
        }

        self.ui_elements = [
            Background(),
            IntroAnimation(),
            GameIdIndicator(self.data["game_id"]),
            GameNameIndicator(self.data["name"]),
            Player1NameIndicator(self.data["players"][0]),
            Player2NameIndicator(None),
            Events(self.data["events"]),
            EventPointerIndicator(self.data["event_pointer"]),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            GameCreatedInGameEvent: self.on_game_created,
            PlayerJoinedInGameEvent: self.on_player_joined,
            PlayerPlacedSymbolInGameEvent: self.on_player_placed_symbol,
        }

    def _process_event(self, event):
        self.events[event.__class__](event)

    def _advance_event_pointer(self):
        self._process_event(self.data["events"][self.data["event_pointer"]])
        if self.data["event_pointer"] < len(self.data["events"]):
            self.data["event_pointer"] += 1

    def on_user_typed(self, event):
        # Avoid circular import
        from client.game.commands import BackToLobby, RequestPlaceASymbol

        if event.key == "return":
            self._advance_event_pointer()
        if event.key == "escape":
            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
        if event.key in "012345678":
            RequestPlaceASymbol(
                self.client_state.profile, self.client_state.queue, event.key
            ).execute()

    def on_game_created(self, event):
        print(
            "New Game created event, do something play some music, update the internal state or something"
        )
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
        # TODO: Could we play a UI animation here???
        self.ui_elements[1].play()
        self.data["events"].append(event)

    def on_player_joined(self, event):
        print(
            "New Player Joined event, do something play some music, update the internal state or something"
        )
        PlaySound(
            self.client_state.profile, self.client_state.queue, "start_game"
        ).execute()
        # self.data.player_2_id = event.player_id
        self.data["events"].append(event)

    def on_player_placed_symbol(self, event):
        print(
            "New Player placed a symbol event, do something play some music, update the internal state or something"
        )
        PlaySound(
            self.client_state.profile, self.client_state.queue, "select"
        ).execute()
        self.data["events"].append(event)
