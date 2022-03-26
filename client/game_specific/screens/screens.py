from abc import ABC
# from .game import Game
from client.game_specific.ui import WelcomeMessage, NewGameMessage, OptionList, ClockUI
from client.game_specific.events import UserTypedEvent

# This should be the definition of the different states


class Screen(ABC):

    def __init__(self, client_state, graphics):
        self.client_state = client_state
        self.graphics = graphics
        # For pygame
        self.ui_elements = []

    def get_ui_elements(self):
        return self.ui_elements

    def render(self):
        self.graphics.render(self)  # Tell graphics to draw current screen

    def update(self, event):
        pass


class Lobby(Screen):

    def __init__(self, client_state, window):
        super().__init__(client_state, window)

        # I think I need some kind of screen dependant set of data
        # for example here I could store the name and the clock value, this data is meant to be displayed.
        # The clock could be relative too. Maybe the strings to be displayed could be stored here too.
        # This data can be initialized and updated per cycle (time).
        self.data = {
            "name": client_state.profile.name,
            "time": client_state.clock.get()
        }

        # This is the graphical representation (pure graphical description). Only for pygame
        self.ui_elements = [
            ClockUI(self.data['time']),
            WelcomeMessage(self.data['name']),
            OptionList({
                "1": "Create a new game",
                "2": "Join an existing game"
            })
        ]

    def update(self, event):
        # And now here I can update the screen-specific data
        # for example the time.
        self.data['time'] = self.client_state.clock.get()

        if event is not None:
            if isinstance(event, UserTypedEvent):
                # Avoid circular import
                # Could these be not just game specific but screen specific?
                from client.game_specific.commands import (
                    NewGame,
                    JoinAGame,
                )
                # These actions, some may update the data, others run commands, who knows
                key = event.key
                if key == "1":
                    NewGame(
                        self.client_state.profile,
                        self.client_state.queue
                    ).execute()
                if key == "2":
                    JoinAGame(self.client_state.profile).execute()

        # Update ui elements (They need to access the data to do so)
        [element.update(self.data) for element in self.ui_elements]


class NewGameScreen(Screen):

    def __init__(self, client_state, window):
        super().__init__(client_state, window)

        self.data = {
            "time": client_state.clock.get(),
            "new_game_name": ""
        }

        self.ui_elements = [
            ClockUI(self.data['time']),
            NewGameMessage(self.data['new_game_name']),
        ]

        # Here if user typed A I would like to update the internal state
        self.actions = {}

    def update(self, event):
        # And now here I can update the screen-specific data
        # for example the time.
        self.data['time'] = self.client_state.clock.get()

        if event is not None:
            if isinstance(event, UserTypedEvent):
                if event.key == "escape":
                    # Avoid circular import
                    from client.game_specific.commands import (
                        BackToLobby
                    )
                    BackToLobby(
                        self.client_state.profile,
                        self.client_state.queue
                    ).execute()
                else:
                    self.data["new_game_name"] += event.key

        # Update ui elements (They need to access the data to do so)
        [element.update(self.data) for element in self.ui_elements]


'''
class InGame(Screen):

    def __init__(self, profile):
        super().__init__(profile)
        self.game = Game()
        # TODO: Import here to avoid circular import
        from .commands import PlaceASymbol, LeaveTheGame
        self.options = {
            '1': PlaceASymbol(self.client_state.profile),
            '2': LeaveTheGame(self.client_state.profile),
        }

    def _print_options(self):
        for index, option in self.options.items():
            print(f'{index} - {option.description}')

    def render(self):
        print('=======================')
        self._print_options()
        print('=======================')

    def _run_command(self, option):
        return self.options[option].execute()

    def update(self, option):
        return self._run_command(option)
'''
