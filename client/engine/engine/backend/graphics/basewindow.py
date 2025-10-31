from abc import ABC, abstractmethod


class BaseWindow(ABC):

    @abstractmethod
    def set_mouse_cursor(self, new_cursor: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def sprite_group(self):
        raise NotImplementedError
