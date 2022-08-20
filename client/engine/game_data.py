from abc import ABC


class GameData(ABC):
    def __init__(self, game_id, name, players=[], events=[]):
        self.id = game_id
        self.name = name
        self.players = players
        self.events = events
