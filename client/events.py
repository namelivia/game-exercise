from client.primitives.event import Event

"""
Events contain an operation and the data needed in order to perform
the operation. Will be put on a queue and when handler will execute
that operation.
"""


# ======= GENERIC =======
class QuitGameEvent(Event):
    pass


class UserTypedEvent(Event):
    def __init__(self, key):
        super().__init__()
        self.key = key


# ======= GAME STATE SYNC =======
class UpdateGameEvent(Event):
    def __init__(self, events):
        super().__init__()
        self.events = events


class InitiateGameEvent(Event):
    def __init__(self, game_data):
        super().__init__()
        self.game_data = game_data


class SetInternalGameInformationEvent(Event):
    def __init__(self, game_id):
        super().__init__()
        self.game_id = game_id


# ===== SERVER INGAME EVENTS COMMUNICATIONS ===== THIS ARE THE IN-GAME EVENTS PLACED BY THE SERVER
class GameCreatedEvent(Event):
    def __init__(self, player_id):
        super().__init__()
        self.player_id = player_id


class PlayerJoinedEvent(Event):
    def __init__(self, player_id):
        super().__init__()
        self.player_id = player_id


# This one seems specific
class PlayerPlacedSymbolEvent(Event):
    def __init__(self, player_id, position):
        super().__init__()
        self.player_id = player_id
        self.position = position


# This one is for polling
class RefreshGameStatusEvent(Event):
    def __init__(self, game_id):
        super().__init__()
        self.game_id = game_id


class NewGameRequestEvent(Event):
    def __init__(self, new_game_name):
        super().__init__()
        self.new_game_name = new_game_name


class JoinExistingGameEvent(Event):
    def __init__(self, game_id):
        super().__init__()
        self.game_id = game_id


# These are network requests
class RefreshGameStatusNetworkRequestEvent(Event):
    def __init__(self, game_id):
        super().__init__()
        self.game_id = game_id


class CreateAGameNetworkRequestEvent(Event):
    def __init__(self, new_game_name):
        super().__init__()
        self.new_game_name = new_game_name


class JoinAGameNetworkRequestEvent(Event):
    def __init__(self, game_id):
        super().__init__()
        self.game_id = game_id