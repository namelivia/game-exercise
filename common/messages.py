
class GameMessage():
    def __init__(self, game):
        self.id = game.id
        self.name = game.name
        self.turn = game.turn
        self.board = game.board
        self.player_1_id = game.player_1_id
        self.player_2_id = game.player_2_id


class CreateAGameMessage():
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id


class JoinAGameMessage():
    def __init__(self, game_id, player_id):
        self.game_id = game_id
        self.player_id = player_id


class PlaceASymbolMessage():
    def __init__(self, game_id, player_id, position):
        self.game_id = game_id
        self.player_id = player_id
        self.position = position


class ErrorMessage():
    def __init__(self, message):
        self.message = message
