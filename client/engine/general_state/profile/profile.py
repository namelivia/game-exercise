from typing import TYPE_CHECKING, Optional

from client.engine.persistence.persistence import Persistence

if TYPE_CHECKING:
    from uuid import UUID


class Profile:
    def __init__(
        self,
        *,
        key: str,
        id: "UUID",
        game_id: Optional["UUID"],
        game_event_pointer: Optional[int],
    ):
        self.key = key
        self.id = id
        self.game_id = game_id
        self.game_event_pointer = game_event_pointer
        self.name: Optional[str] = None

    def set_game(self, game_id: Optional["UUID"]) -> None:
        self.game_id = game_id

    def set_name(self, name: str) -> None:
        self.name = name
        self.save()

    def set_game_event_pointer(self, game_event_pointer: Optional[int]) -> None:
        self.game_event_pointer = game_event_pointer

    def save(self) -> None:
        Persistence.save(self, self.key)
