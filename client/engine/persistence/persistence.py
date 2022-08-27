import pickle
from os import walk
from .persistence_dto import PersistenceDTO

PATH = "client_data/"


class Persistence:
    @staticmethod
    def load(key) -> PersistenceDTO:
        return pickle.load(open(f"{PATH}{key}", "rb"))

    @staticmethod
    def save(data: PersistenceDTO, key):
        pickle.dump(data, open(f"{PATH}{key}", "wb"))

    @staticmethod
    def list():
        return next(walk(PATH))[2]
