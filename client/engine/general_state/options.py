from typing import Any, Tuple, Type

from client.engine.persistence.options_persistence import OptionsPersistence


class Options:
    _instance = None

    # This class is a singleton
    def __new__(cls: Type["Options"], *args: Any, **kwargs: Any) -> "Options":
        if not cls._instance:
            cls._instance = super(Options, cls).__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        self.sound_on = False  # Sound off by default

    def set_sound_on(self) -> None:
        self.sound_on = True
        self._save()

    def set_sound_off(self) -> None:
        self.sound_on = False
        self._save()

    def _save(self) -> None:
        OptionsPersistence.save(self)
