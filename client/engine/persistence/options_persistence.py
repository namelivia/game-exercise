import pickle
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.engine.general_state.options import Options

PATH = "client_data/"


class OptionsPersistence:
    @staticmethod
    def load() -> "Options":
        data = pickle.load(open(f"{PATH}options", "rb"))

        # avoid circlar dependency
        from client.engine.general_state.options import Options

        if isinstance(data, Options):
            return data
        raise Exception("Loaded something that is not options")

    @staticmethod
    def save(data: "Options") -> None:
        pickle.dump(data, open(f"{PATH}options", "wb"))
