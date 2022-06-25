class GameMessage:
    def __init__(self, game):
        self.id = game.id
        self.name = game.name
        self.players = game.players
        self.events = game.events


class GameListMessage:
    def __init__(self, game_list):
        self.game_list = game_list


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
