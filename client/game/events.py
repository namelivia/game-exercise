from client.primitives.event import Event

"""
Events contain an operation and the data needed in order to perform
the operation. Will be put on a queue and when handler will execute
that operation.
"""


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


class ClearInternalGameInformationEvent():
    pass


class PlaceASymbolNetworkRequestEvent(Event):
    def __init__(self, game_id, position):
        super().__init__()
        self.game_id = game_id
        self.position = position


class CreateAGameNetworkRequestEvent(Event):
    def __init__(self, new_game_name):
        super().__init__()
        self.new_game_name = new_game_name


class JoinAGameNetworkRequestEvent(Event):
    def __init__(self, game_id):
        super().__init__()
        self.game_id = game_id


class RefreshGameStatusNetworkRequestEvent(Event):
    def __init__(self, game_id):
        super().__init__()
        self.game_id = game_id


class JoinExistingGameEvent(Event):
    def __init__(self, game_id):
        super().__init__()
        self.game_id = game_id


class RefreshGameStatusEvent(Event):
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
            events,
            player_1_id,
            player_2_id,
    ):
        super().__init__()
        self.game_id = game_id
        self.name = name
        self.turn = turn
        self.board = board
        self.events = events
        self.player_1_id = player_1_id
        self.player_2_id = player_2_id


class UpdateGameEvent(Event):
    def __init__(
            self,
            game_id,
            name,
            turn,
            board,
            events,
            player_1_id,
            player_2_id,
    ):
        super().__init__()
        self.game_id = game_id
        self.name = name
        self.turn = turn
        self.board = board
        self.events = events
        self.player_1_id = player_1_id
        self.player_2_id = player_2_id


class GameCreatedEvent(Event):
    def __init__(
            self,
            player_id
    ):
        super().__init__()
        self.player_id = player_id


class PlayerJoinedEvent(Event):
    def __init__(
            self,
            player_id
    ):
        super().__init__()
        self.player_id = player_id


class PlayerPlacedSymbolEvent(Event):
    def __init__(
            self,
            player_id,
            position
    ):
        super().__init__()
        self.player_id = player_id
        self.position = position


class PlaySoundEvent(Event):
    def __init__(
            self,
            sound
    ):
        super().__init__()
        self.sound = sound
