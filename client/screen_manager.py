from .screens import Lobby, InGame


class ScreenManager():

    def __init__(self, profile):
        self.profile = profile
        self.current_screen = Lobby(self.profile)

    def go_to(self, key):
        if key == 'lobby':
            self.current_screen = Lobby(self.profile)
        if key == 'in_game':
            self.current_screen = InGame(self.profile)

    def run(self):
        self.current_screen.render()
        input_data = self.current_screen.read_input()
        if self.current_screen.is_invalid_option(input_data):
            print('Invalid option')
            return None

        # Update state
        new_screen = self.current_screen.run_command(input_data)
        if new_screen is not None:
            self.go_to(new_screen)
