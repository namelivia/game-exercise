from abc import ABC
from .screens import Lobby, NewGameScreen


class Event(ABC):

    def __init__(self):
        pass

    def execute():
        pass


class ScreenTransitionEvent(Event):
    def __init__(self, dest_screen):
        super().__init__()
        self.dest_screen = dest_screen

    # Actually only this mapping is game_specific
    def execute(self, client_state, graphics):
        if self.dest_screen == "lobby":
            return Lobby(client_state, graphics)
        if self.dest_screen == "new_game_screen":
            return NewGameScreen(client_state, graphics)
