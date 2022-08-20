import pickle
from .persistence_dto import PersistenceDTO

PATH = "client_data/profile"


class Persistence:
    @staticmethod
    def load() -> PersistenceDTO:
        return pickle.load(open(PATH, "rb"))

    @staticmethod
    def save(data: PersistenceDTO):
        pickle.dump(data, open(PATH, "wb"))
