from abc import ABC


class Event(ABC):
    pass


class QuitGameEvent(Event):
    pass


class ScreenTransitionEvent(Event):
    def __init__(self, dest_screen):
        super().__init__()
        self.dest_screen = dest_screen


class UserTypedEvent(Event):
    def __init__(self, key):
        super().__init__()
        self.key = key


class NewGameRequestEvent(Event):
    def __init__(self, new_game_name):
        super().__init__()
        self.new_game_name = new_game_name


class PlaceASymbolRequestEvent(Event):
    def __init__(self, position):
        super().__init__()
        self.position = position


class JoinExistingGameEvent(Event):
    def __init__(self, game_id):
        super().__init__()
        self.game_id = game_id


class InitiateGameEvent(Event):
    def __init__(
            self,
            game_id,
            name,
            turn,
            board,
            player_1_id,
            player_2_id,
    ):
        super().__init__()
        self.game_id = game_id
        self.name = name
        self.turn = turn
        self.board = board
        self.player_1_id = player_1_id
        self.player_2_id = player_2_id
