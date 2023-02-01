from typing import TYPE_CHECKING, List, Any

if TYPE_CHECKING:
    from uuid import UUID
    from common.game_data import GameData


class GameInfoMessage:
    def __init__(self, game: "GameData"):
        self.id = game.id
        self.name = game.name
        self.players = game.players


class GameEventsMessage:
    def __init__(self, events: List[Any]):
        self.events = events  # TODO: This could be too big for the channel


class GameListMessage:
    def __init__(self, game_list: List[str]):
        self.game_list = game_list  # TODO: This could be too big for the channel


class CreateAGameMessage:
    def __init__(self, name: str, player_id: "UUID"):
        self.name = name
        self.player_id = player_id


class JoinAGameMessage:
    def __init__(self, game_id: "UUID", player_id: "UUID"):
        self.game_id = game_id
        self.player_id = player_id


class PlaceASymbolMessage:
    def __init__(
        self, game_id: "UUID", event_id: "UUID", player_id: "UUID", position: int
    ):
        self.game_id = game_id
        self.event_id = event_id
        self.player_id = player_id
        self.position = position


class SendChatMessage:
    def __init__(
        self, game_id: "UUID", event_id: "UUID", player_id: "UUID", message: str
    ):
        self.game_id = game_id
        self.event_id = event_id
        self.player_id = player_id
        self.message = message


class ChatMessageConfirmation:
    def __init__(self, event_id: "UUID"):
        self.event_id = event_id


class SymbolPlacedConfirmation:
    def __init__(self, event_id: "UUID"):
        self.event_id = event_id


class ChatMessageError:
    def __init__(self, event_id: "UUID"):
        self.event_id = event_id


class ErrorMessage:
    def __init__(self, message: str):
        self.message = message


class GetGameStatus:
    def __init__(self, game_id: "UUID", pointer: int, player_id: "UUID"):
        self.game_id = game_id
        self.pointer = pointer
        self.player_id = player_id


class PingRequestMessage:
    pass


class PingResponseMessage:
    pass


class GameListRequestMessage:
    pass


class GameListResponseEntry:
    def __init__(self, game: "GameData"):
        self.id = game.id
        self.name = game.name


class GameListResponseMessage:
    def __init__(self, games: List[GameListResponseEntry]):
        self.games = games  # TODO:  This could be too big for the channel
