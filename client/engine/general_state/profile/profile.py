from client.engine.persistence.persistence import Persistence


class Profile:
    def __init__(
        self,
        *,
        key: str,
        id: str,
        game_id: str,
        game_event_pointer: int,
        sound_on: bool
    ):
        self.key = key
        self.id = id
        self.game_id = game_id
        self.game_event_pointer = game_event_pointer
        self.sound_on = sound_on
        self.name = None

    def set_game(self, game_id: str) -> None:
        self.game_id = game_id

    def set_name(self, name: str) -> None:
        self.name = name
        self.save()

    def set_game_event_pointer(self, game_event_pointer: int) -> None:
        self.game_event_pointer = game_event_pointer

    def set_sound_on(self) -> None:
        self.sound_on = True
        self.save()

    def set_sound_off(self) -> None:
        self.sound_on = False
        self.save()

    def save(self) -> None:
        Persistence.save(self, self.key)
