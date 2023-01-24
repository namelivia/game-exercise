import pickle
from typing import TYPE_CHECKING, Iterable
from os import walk

if TYPE_CHECKING:
    from .persistence_dto import PersistenceDTO

PATH = "client_data/"


class Persistence:
    @staticmethod
    def load(key: str) -> "PersistenceDTO":
        return pickle.load(open(f"{PATH}{key}", "rb"))

    @staticmethod
    def save(data: "PersistenceDTO", key: str) -> None:
        pickle.dump(data, open(f"{PATH}{key}", "wb"))

    @staticmethod
    def list() -> Iterable:
        return next(walk(PATH))[2]
