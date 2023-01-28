import pickle
from typing import TYPE_CHECKING, Iterable
from os import walk

if TYPE_CHECKING:
    from client.engine.general_state.profile.profile import Profile

PATH = "client_data/"


class Persistence:
    @staticmethod
    def load(key: str) -> "Profile":
        data = pickle.load(open(f"{PATH}{key}", "rb"))
        if isinstance(data, Profile):
            return data
        raise Exception("Loaded something that is not a profile")

    @staticmethod
    def save(data: "Profile", key: str) -> None:
        pickle.dump(data, open(f"{PATH}{key}", "wb"))

    @staticmethod
    def list() -> Iterable[str]:
        return next(walk(PATH))[2]
