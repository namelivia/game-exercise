from client.engine.primitives.event import Event

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


class TurnSoundOnEvent(Event):
    pass


class TurnSoundOffEvent(Event):
    pass


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
class GameCreatedInGameEvent(Event):
    def __init__(self, player_id):
        super().__init__()
        self.player_id = player_id


class PlayerJoinedInGameEvent(Event):
    def __init__(self, player_id):
        super().__init__()
        self.player_id = player_id


class PlayerWinsInGameEvent(Event):
    def __init__(self, player_id):
        super().__init__()
        self.player_id = player_id


# This one seems specific
class PlayerPlacedSymbolInGameEvent(Event):
    def __init__(self, player_id, position):
        super().__init__()
        self.player_id = player_id
        self.position = position


class ChatMessageInGameEvent(Event):
    def __init__(self, player_id, message):
        super().__init__()
        self.player_id = player_id
        self.message = message


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


class PingNetworkRequestEvent(Event):
    pass


class GetGameListNetworkRequestEvent(Event):
    pass


class ErrorGettingGameListEvent(Event):
    pass


class ErrorCreatingGameEvent(Event):
    pass


class ErrorJoiningGameEvent(Event):
    pass


class UpdateGameListEvent(Event):
    def __init__(self, games):
        super().__init__()
        self.games = games


class SetPlayerNameEvent(Event):
    def __init__(self, name):
        super().__init__()
        self.name = name


class GetProfilesEvent(Event):
    pass


class ProfilesUpdatedEvent(Event):
    def __init__(self, profiles):
        super().__init__()
        self.profiles = profiles


class UpdateProfilesInGameEvent(Event):
    def __init__(self, profiles):
        super().__init__()
        self.profiles = profiles


class SetProfileEvent(Event):
    def __init__(self, key):
        super().__init__()
        self.key = key


class NewProfileEvent(Event):
    pass


class ProfileSetInGameEvent(Event):
    def __init__(self, key):
        super().__init__()
        self.key = key
