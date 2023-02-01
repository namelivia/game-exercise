from abc import ABC
from typing import List
from uuid import UUID


class GameData(ABC):
    def __init__(
        self,
        game_id: UUID,
        name: str,
        players: List[UUID] = [],
        events: List[UUID] = [],
    ):
        self.id = game_id
        self.name = name
        self.players = players
        self.events = events
