from abc import ABC


class GameData(ABC):
    def __init__(self, game_id, name, player_1_id, player_2_id, events=[]):
        self.id = game_id
        self.name = name
        self.player_1_id = player_1_id
        self.player_2_id = player_2_id
        self.events = events
