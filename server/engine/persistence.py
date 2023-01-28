import pickle
from os import walk
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from server.game.game import Game

GAMES_PATH = "server_data/games/"


class Persistence:
    @staticmethod
    def load_game(game_id: str) -> "Game":
        data = pickle.load(open(f"{GAMES_PATH}{game_id}", "rb"))
        if isinstance(data, Game):
            return data
        raise Exception("Loaded something that is not a game")

    @staticmethod
    def save_game(new_game: "Game") -> None:
        pickle.dump(new_game, open(GAMES_PATH + str(new_game.id), "wb"))

    @staticmethod
    def get_all_games() -> Iterable[str]:
        return next(walk(GAMES_PATH))[2]
