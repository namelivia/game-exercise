from abc import ABC, abstractmethod


class BaseGraphicsBackend(ABC):

    @abstractmethod
    def update_display(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_new_window(self, width: int, height: int):
        raise NotImplementedError

    @abstractmethod
    def clear_window(self, window):
        raise NotImplementedError
