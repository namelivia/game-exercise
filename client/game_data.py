from abc import ABC


class GameData(ABC):
    def __init__(self, game_id, events):
        self.id = game_id
        self.events = events
