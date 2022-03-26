import pygame
from abc import ABC
# from .game import Game
from client.game_specific.ui import WelcomeMessage, NewGameMessage, OptionList, ClockUI

# This should be the definition of the different states


class Screen(ABC):

    def __init__(self, client_state, graphics):
        self.client_state = client_state
        self.graphics = graphics
        # For pygame
        self.ui_elements = []

        # For text mode
        self.text_elements = []

    def get_text_elements(self):
        return self.text_elements

    def get_ui_elements(self):
        return self.ui_elements

    def render(self):
        self.graphics.render(self)  # Tell graphics to draw current screen

    def update(self, events):
        # Transform events into actions
        if events is not None:
            for event in events:
                action = self._get_action(event)
                if action is not None:
                    action.execute()

    def _get_action(self, event):
        # Map pygame events with actions
        # This may change based on the clock
        try:
            return self.mapping[event]
        except KeyError:
            pass


class Lobby(Screen):

    def __init__(self, client_state, window):
        super().__init__(client_state, window)

        # This is the graphical representation (pure graphical description). Only for pygame
        self.ui_elements = [
            ClockUI(self.client_state.clock),
            WelcomeMessage(),
            OptionList({
                "1": "Create a new game",
                "2": "Join an existing game"
            })
        ]

        # This is the text representation (pure graphical description). Only for text mode
        self.text_elements = [
            "Welcome to game",
            "1: Create a new game",
            "2: Join an existing game",
        ]

        # This is the functional representation (input and actions). (Will always be here)
        # Avoid circular import
        from client.game_specific.commands import (
            NewGame,
            JoinAGame,
        )
        self.mapping = {
            "event_1": NewGame(self.client_state.profile, self.client_state.queue),  # These will always end up adding events to the queue
            "event_2": JoinAGame(self.client_state.profile),
        }


class NewGameScreen(Screen):

    def __init__(self, client_state, window):
        super().__init__(client_state, window)

        # local Screen state
        self.new_game_name = ""

        # This is the text representation (pure graphical description). Only for text mode
        self.ui_elements = [
            ClockUI(self.client_state.clock),
            NewGameMessage(),
        ]

        # This is the text representation (pure graphical description). Only for text mode
        self.text_elements = [
            "Create a new game",
            "Please write the name for your new game",
        ]

        # TODO: This does not work
        # This is the functional representation (input and actions). (Will always be here)
        # Avoid circular import
        # from .commands import (
        # AddLetterA,  # These commands may be screen dependent
        # )
        # self.mapping = {pygame.A: {
        # pygame.K_A: AddLetterA(self.client_state.profile, self.client_state.queue),  # Will These will always adding events to the queue?
        # }}
        self.mapping = {}


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
