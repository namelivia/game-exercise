from abc import ABC
from typing import List


class GameData(ABC):
    def __init__(
        self, game_id: str, name: str, players: List[str] = [], events: List[str] = []
    ):
        self.id = game_id
        self.name = name
        self.players = players
        self.events = events
