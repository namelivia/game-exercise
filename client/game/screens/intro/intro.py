from client.engine.primitives.screen import Screen
from client.game.commands import PlaySound, PlayMusic
from .ui import Title, Background, Coins
from client.engine.events import UserTypedEvent


class Intro(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)

        self.ui_elements = [
            Background(),
            Coins(),
            Title(self.time),
        ]

        PlayMusic(
            self.client_state.profile, self.client_state.queue, "main_theme"
        ).execute()

        self.timers = {
            10000: self.show_coins,
            30000: self.go_back_to_lobby,
        }

        self.events = {UserTypedEvent: self.on_user_typed}

    # Actions
    def go_back_to_lobby(self):
        from client.game.commands import BackToLobby

        BackToLobby(self.client_state.profile, self.client_state.queue).execute()

    def show_coins(self):
        PlaySound(
            self.client_state.profile, self.client_state.queue, "user_joined"
        ).execute()
        self.ui_elements[1].appear()

    def on_user_typed(self, event):
        if event.key == "escape" or event.key == "return":
            # Avoid circular import
            from client.game.commands import ToLobby

            ToLobby(self.client_state.profile, self.client_state.queue).execute()
