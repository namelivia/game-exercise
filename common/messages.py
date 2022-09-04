class GameInfoMessage:
    def __init__(self, game):
        self.id = game.id
        self.name = game.name
        self.players = game.players


class GameEventsPageMessage:
    def __init__(self, events):
        self.events = events  # TODO: This could be too big for the channel


class GameListPageMessage:
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
    def __init__(self, game_id, player_id, message):
        self.game_id = game_id
        self.player_id = player_id
        self.message = message


class ErrorMessage:
    def __init__(self, message):
        self.message = message


class GetGameStatus:
    def __init__(self, game_id, player_id):
        self.game_id = game_id
        self.player_id = player_id


class PingRequestMessage:
    pass


class PingResponseMessage:
    pass


class GameListRequestMessage:
    pass


class GameListResponsePageMessage:
    def __init__(self, games):
        self.games = games  # TODO:  This could be too big for the channel


class GameListResponseEntry:
    def __init__(self, game):
        self.id = game.id
        self.name = game.name
