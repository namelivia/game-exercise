class GameInfoMessage:
    def __init__(self, game):
        self.id = game.id
        self.name = game.name
        self.players = game.players


class GameEventsMessage:
    def __init__(self, events):
        self.events = events  # TODO: This could be too big for the channel


class GameListMessage:
    def __init__(self, game_list):
        self.game_list = game_list  # TODO: This could be too big for the channel


class CreateAGameMessage:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id


class JoinAGameMessage:
    def __init__(self, game_id, player_id):
        self.game_id = game_id
        self.player_id = player_id


class PlaceASymbolMessage:
    def __init__(self, game_id, player_id, position):
        self.game_id = game_id
        self.player_id = player_id
        self.position = position


class SendChatMessage:
    def __init__(self, game_id, event_id, player_id, message):
        self.game_id = game_id
        self.event_id = event_id
        self.player_id = player_id
        self.message = message


class ChatMessageConfirmation:
    def __init__(self, event_id, player_id, message):
        self.event_id = event_id
        self.player_id = player_id
        self.message = message


class ChatMessageError:
    def __init__(self, event_id):
        self.event_id = event_id


class ErrorMessage:
    def __init__(self, message):
        self.message = message


class GetGameStatus:
    def __init__(self, game_id, pointer, player_id):
        self.game_id = game_id
        self.pointer = pointer
        self.player_id = player_id


class PingRequestMessage:
    pass


class PingResponseMessage:
    pass


class GameListRequestMessage:
    pass


class GameListResponseMessage:
    def __init__(self, games):
        self.games = games  # TODO:  This could be too big for the channel


class GameListResponseEntry:
    def __init__(self, game):
        self.id = game.id
        self.name = game.name
