import pickle
from .persistence_dto import PeristenceDTO

PATH = "client_data/profile"


class Peristence:
    @staticmethod
    def load() -> PeristenceDTO:
        return pickle.load(open(PATH, "rb"))

    @staticmethod
    def save(data: PeristenceDTO):
        pickle.dump(data, open(PATH, "wb"))
