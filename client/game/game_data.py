from client.game_data import GameData


class CustomGameData(GameData):
    def __init__(self, game_id, name, turn, board, player_1_id, player_2_id, events=[]):
        super().__init__(game_id, events)
        self.name = name
        self.turn = turn
        self.board = board
        self.player_1_id = player_1_id
        self.player_2_id = player_2_id
