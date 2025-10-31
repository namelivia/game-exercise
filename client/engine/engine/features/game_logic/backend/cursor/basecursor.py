from abc import ABC, abstractmethod


class BaseCursor(ABC):

    @abstractmethod
    def set_mouse_cursor(self, new_cursor: str) -> None:
        raise NotImplementedError
