from abc import ABC
from .game import Game


class Screen(ABC):

    def __init__(self, profile):
        self.profile = profile

    def render(self):
        pass

    def read_input(self):
        pass

    def is_invalid_option(self, option):
        pass

    def run_command(self, option):
        pass


class Lobby(Screen):

    def __init__(self, profile):
        super().__init__(profile)
        from .commands import (
            CreateAGame,
            JoinAGame,
        )

        # TODO: import here to avoid circular import
        self.options = {
            '1': CreateAGame(self.profile),
            '2': JoinAGame(self.profile),
        }

    def _print_options(self):
        for index, option in self.options.items():
            print(f'{index} - {option.description}')

    def render(self):
        print('[WELCOME TO GAME]')
        print('=======================')
        self._print_options()
        print('=======================')

    def read_input(self):
        return input("Select an option:")

    def is_invalid_option(self, option):
        return option not in self.options.keys()

    def run_command(self, option):
        return self.options[option].execute()


class InGame(Screen):

    def __init__(self, profile):
        super().__init__(profile)
        self.game = Game()
        # TODO: Import here to avoid circular import
        from .commands import PlaceASymbol, LeaveTheGame
        self.options = {
            '1': PlaceASymbol(self.profile),
            '2': LeaveTheGame(self.profile),
        }

    def _print_options(self):
        for index, option in self.options.items():
            print(f'{index} - {option.description}')

    def render(self):
        print('=======================')
        self._print_options()
        print('=======================')

    def read_input(self):
        self.game.render()
        self.render()
        return input("Select an option:")

    def is_invalid_option(self, option):
        return option not in self.options.keys()

    def run_command(self, option):
        return self.options[option].execute()
